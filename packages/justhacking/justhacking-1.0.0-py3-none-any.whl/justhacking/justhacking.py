# Importing main libraries
import time, sys, itertools, threading, progressbar, random, tkinter

# Module for alert box
from tkinter import messagebox

# Loading effect support modules
from tqdm import tqdm

# import only system from os
from os import system, name


def clear():
  # for windows
  if name == 'nt':
    _ = system('cls')
  
  # for mac and linux(here, os.name is 'posix')
  else:
    _ = system('clear')

# Banner
def banner():
  print('''
░░█ █░█ █▀ ▀█▀   █░█ █░█ █▀▀ █▄▀ ▄█ █▄░█ █▀▀
█▄█ █▄█ ▄█ ░█░   █▀█ ▀▀█ █▄▄ █░█ ░█ █░▀█ █▄█
  ''')
  time.sleep(1)
  clear()

# Typing Effect (https://github.com/Divinemonk/typewriter.py)
def typit(text):
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)

def dot_loading():
  done = False
  #here is the animation
  def animate():
      for c in itertools.cycle(['|', '/', '-', '\\']):
          if done:
              break
          sys.stdout.write('\r[#] Hacking System ' + c)
          sys.stdout.flush()
          time.sleep(0.1)
      sys.stdout.write('\n[!] Target found !    ')
      time.sleep(0.2)

  t = threading.Thread(target=animate)
  t.start()

  #long process here
  time.sleep(4)
  done = True

# Loading bar
def tqdm_loading(description):
  for i in tqdm (range (65535), desc=description):
    pass


def alert(title, message):
  # This code is to hide the main tkinter window
  root = tkinter.Tk()
  root.withdraw()
  # message
  messagebox.showinfo(title, message)
  time.sleep(3)
  root.destroy() 


# Main Logical flow
def starthack():
  banner()
  typit('[#] Hacking System')
  dot_loading()
  tqdm_loading('\n[%] Scanning target network')
  typit('[+] Network Vulnerable\n > Setting up hacks to crack into the network')
  time.sleep(0.5)
  typit('.........')
  time.sleep(0.5)
  typit('\n[!] Cracking into the network\n > Hijacking sys inet ports 46654-65535 ')
  time.sleep(0.5)
  typit('.........')
  time.sleep(0.2)
  typit('\n[FPD Alert] Firewall Protection Detected !')
  time.sleep(0.1)
  typit('\n[:)] Cracking Firewall in : 3   2   1')
  time.sleep(0.1)
  typit('\n[FPD Vulnerable with ixss photom circuits]')
  time.sleep(0.3)
  typit('\n-----------Deactivating-------Firewall--------------')
  time.sleep(0.2)
  typit('\n[+] Firewall Deactivated successfully')
  time.sleep(0.2)
  alert('Attack Results', 'System got Hacked\nGained os full access')
  typit('\n[!] System got Hacked Gained os full access')
  clear()
  typit("Follow on Twitter: @HrDivinemonk")
  typit('\nGive a star on Pypi & Github\nhttps://github.com/divinemonk/justhacking')
  time.sleep(5)
  typit('\n\n      [Hacker is Back]\n')
  banner()

starthack()