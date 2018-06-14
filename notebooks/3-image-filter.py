# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:43:31 2018

@author: carlos.m.s.quintos
"""
import cv2
import numpy as np


def apply_invert(frame):
    return cv2.bitwise_not(frame)

def apply_sepia(frame, intensity = 0.5):
    blue, green, red = 20, 66, 112
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame = apply_alpha_convert(frame)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width,4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0,0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def apply_burgundy(frame, intensity = 0.5):
    blue, green, red = 32, 0, 200
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_height, frame_width, frame_channel = frame.shape
    sepia_bgra = (blue, green, red, 1)
    
    overlay = np.full((frame_height, frame_width,4), sepia_bgra, dtype='uint8')
    
    frame = cv2.addWeighted(overlay, intensity, frame, 1.0,0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    return frame

def apply_alpha_convert(frame):
    try:
        frame.shape[3]
    except IndexError:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        return frame

def apply_portrait_mode_mask(frame):
    frame = apply_alpha_convert(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    
    return mask
    
def apply_portrait_mode_blurred(frame):
    frame = apply_alpha_convert(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(frame, (21,21), 0)
    
    return blurred

def apply_portrait_mode_blend(frame):
    frame = apply_alpha_convert(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blurred = cv2.GaussianBlur(frame, (21,21), 0)
    
    blended = apply_blend(frame, blurred, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame

def apply_blend(frame_1, frame_2, mask):
    alpha = mask / 255.0
    blended = cv2.convertScaleAbs(frame_1 * (1 - alpha) + (frame_2 * alpha))
    return blended

def show_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        
        invert = apply_invert(frame)
        sepia = apply_sepia(frame)        
        bur = apply_burgundy(frame)
        blur = apply_portrait_mode_blurred(frame)
        gray = apply_portrait_mode_mask(frame)
        blend = apply_portrait_mode_blend(frame)
        
        cv2.imshow('true', frame)
        cv2.imshow('invert', invert)
        cv2.imshow('sep', sepia)
        cv2.imshow('bur', bur)
        cv2.imshow('blur', blur)
        cv2.imshow('gray', gray)
        cv2.imshow('blend', blend)

        if cv2.waitKey(1) == 27:        
            cap.release()
            cv2.destroyAllWindows()
            break
        
show_webcam()