import numpy as np
import cv2


class convert:
    def __init__(self,image):
        self.im = cv2.imread(image,0)
        self.ret,self.im = cv2.threshold(self.im,127,255,cv2.THRESH_BINARY)
    def corners(self):
        h,w = self.im.shape[0:2]
        rowsums=np.empty((h))      
        np.sum(self.im,axis=1,out=rowsums)        
        rowsums /= np.max(rowsums)/100      
        firsty = lasty = -1
        for r in range(h):
            if firsty < 0 and rowsums[r] < 50:
                firsty = r
            if rowsums[r] < 50:
                lasty = r+1
        colsums=np.empty((w))      
        np.sum(self.im,axis=0,out=colsums)        
        colsums /= np.max(colsums)/100      
        firstx = lastx = -1
        for c in range(w):
            if firstx < 0 and colsums[c] < 50:
                firstx = c
            if colsums[c] < 50:
                lastx = c+1
        return firstx,firsty,lastx,lasty
    def coun(self,lis):
        width = 0
        self.count = 0
        for x in lis:
            if x == 0:
                self.count += 1
                if self.count > width:
                    width = self.count
            else:
                self.count = 0
        return width
    def coords(self,lis):
        self.count = 0
        width = 0
        s= 0
        for y,x in enumerate(lis):
            if x == 0:
                self.count+=1
                if self.count > width:
                    width = self.count
                    s = y- width//2
                else:
                    self.count = 0
        return s
    def finding(self,lis):
        x = lis.index(max(lis))
        if x == 0:
            return self.coords(self.im[0]),0
        if x ==1:
            return 0,self.coords(self.im[:,0])
        if x ==2:
            return self.coords(self.im[-1]),-1
        else:
            return -1,self.coords(self.im[:,-1])
    def clean(self):
        x,y,x2,y2 = self.corners()
        self.im[self.im == 0] = 1
        self.im[self.im == 255] = 0
        self.im = self.im[y:y2, x:x2]
        self.counts = [self.coun(self.im[0]),self.coun(self.im[:,0]), self.coun(self.im[-1]),self.coun(self.im[:,-1])]
        sx,sy = self.finding(self.counts)
        self.counts[self.counts.index(max(self.counts))] = 0
        ex,ey = self.finding(self.counts)
        self.im[sy][sx]=2
        self.im[ey][ex]=3
        self.im[sy][sx]=2
        self.im[ey][ex]=3
        return self.im
    
    
