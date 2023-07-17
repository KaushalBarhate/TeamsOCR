from datetime import datetime
import os
from threading import Timer
import winsound
from PIL import ImageGrab
import pyperclip
import cv2
import pytesseract
from PIL import Image 
import timer

    
 
# Check image folder exists in current directory.
img_folder = 'clipboard_images'
#img_folder = 'C:/Users/Kaushal Barhate/OneDrive/clipboard_images'
check_img_folder = os.path.isdir(img_folder)
 
# If it doesn't exist, then create it.
if not check_img_folder:
    os.makedirs(img_folder)
    print('created folder : ', img_folder)
 
# Check text folder exists in current directory.
txt_folder = 'clipboard_texts'
check_txt_folder = os.path.isdir(txt_folder)
 
# If it doesn't exist, then create it.
if not check_txt_folder:
    os.makedirs(txt_folder)
    print('created folder : ', txt_folder)
 
def beep_sound():
    """Beep sound. frequency, duration."""
    winsound.Beep(840, 100)
 
def save_cb_text():
    """If text found on clipboard, Save to uniquely named text file."""
    # Grab clipboard contents.
    cb_txt = pyperclip.paste()
    
 
    if cb_txt:
        tits = '-' *34+'\n'
        # I wanted a properly readable date and time as the file name.
        time_stamp = (datetime.now().strftime
                      (r'%d'+('-')+'%b'+('-')+'%Y'+('-')+'%H'+('.')
                       +'%M'+('-')+'%S'+'s'))
 
        file_name = time_stamp+'.txt'
        folder = r'clipboard_texts/'
 
        with open(folder+str(file_name), 'w') as contents:
            contents.write('Clipboard text found: '+str(time_stamp)+'\n')
            contents.write(tits)
            contents.write(cb_txt)
            #beep_sound()
 
            print('Clipboard text found and saved as', file_name)
 
            # Clear clipboard.
            pyperclip.copy('')
def imgcrop():
    file_name2 = (datetime.now().strftime
                     (r'%d'+('-')+'%b'+('-')+'%Y'+('-')))+'.jpg'
    str2="C:/Users/Kaushal Barhate/.spyder-py3/clipboard_images/"+file_name2
    im = Image.open(str2) 
  
# Size of the image in pixels (size of orginal image) 
# (This is not mandatory) 
    width, height = im.size 
  
# Setting the points for cropped image 
    left = 5
    top = height / 6
    right = 1750
    bottom = 3 * height / 4
  
# Cropped image of above dimension 
# (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom)) 
    im1.save(str2)
def ocr():
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    file_name1 = (datetime.now().strftime
                     (r'%d'+('-')+'%b'+('-')+'%Y'+('-')))+'.jpg'
    str="C:/Users/Kaushal Barhate/.spyder-py3/clipboard_images/"+file_name1

    img1 = cv2.imread(str)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
												cv2.CHAIN_APPROX_NONE)
    im2 = img1.copy()
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = im2[y:y + h, x:x + w]
        file = open("C:/Users/Kaushal Barhate/OneDrive/recognized.txt", "a")
        text = pytesseract.image_to_string(cropped)
        file.write(text)
        file.write("\n")
        file.close()
	
 
def grab_cb_img():
    """If image found, Save to uniquely named jpg file."""
    # Grab clipboard.
    img = ImageGrab.grabclipboard()
    
    # If an image is found on the clipboard...
    if img:
        #if img.mode != 'RGB':
         #   img = img.convert('RGB')
        # Create unique file name using current date and time.
        file_name = (datetime.now().strftime
                     (r'%d'+('-')+'%b'+('-')+'%Y'+('-')))+'.jpg'
 
        folder = r'clipboard_images/'
        img.save(folder+file_name)
        #beep_sound()
 
        print('Clipboard image found and saved as', file_name)
        
 
        # Clear clipboard so that same image is not saved again.
        pyperclip.copy('')
        imgcrop()
        ocr()
        
       
        
            
 
def grab_img():
    """Main loop using 1 second timer to check clipboard."""
    grab_cb_img()
    save_cb_text()
 
    grab_timer = Timer(1, grab_img)
    grab_timer.start()
    
grab_img()
