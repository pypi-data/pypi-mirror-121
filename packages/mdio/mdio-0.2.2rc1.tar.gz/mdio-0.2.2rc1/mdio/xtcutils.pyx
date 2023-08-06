cdef class BitByteBuffer(object):
    cdef unsigned char[:] ba
    cdef int lastbyte
    cdef int lastbits
    cdef int cnt
    cdef int lba
    cdef int linc
    
    def __init__(self, unsigned char[:] byts):
        self.ba = byts
        self.lastbyte = 0
        self.lastbits = 0
        self.cnt = 0
        self.lba = self.ba.shape[0]
        self.linc = self.lba // 5
        
    def receiveint(self, int nbits):
        cdef int num = 0
        cdef int mask = (1<< nbits) -1
        cdef int lastbyte = self.lastbyte
        cdef int lastbits = self.lastbits
        cdef int cnt = 0
        cdef unsigned char[:] ba = self.ba[self.cnt:self.cnt+32]
        
        while nbits >= 8:
            lastbyte = ( lastbyte << 8) | ba[cnt]
            cnt += 1
            num |= (lastbyte >> lastbits) << (nbits - 8)
            nbits -= 8
        if nbits > 0:
            if lastbits < nbits:
                lastbits += 8
                lastbyte = (lastbyte << 8) | ba[cnt]
                cnt += 1
            lastbits -= nbits
            num |= (lastbyte >> lastbits) & ((1 << nbits) -1)
        num &= mask
        lastbyte &= 0xff
        self.lastbyte = lastbyte
        self.lastbits = lastbits
        self.cnt += cnt
        return num
    
    def sendint(self, int nbits, int num):
        
        cdef int nbytes = (nbits + 7) // 8 + 1
        cdef int cnt = 0
        cdef int lastbyte = self.lastbyte
        cdef int lastbits = self.lastbits
        cdef unsigned char[32] ba 
        cdef int j
        while nbits >= 8:
            lastbyte = (lastbyte << 8) | (num >> (nbits - 8))
            ba[cnt] = (lastbyte >> lastbits) & 0xff
            cnt += 1
            nbits -= 8
        if nbits > 0:
            lastbyte = (lastbyte << nbits) | num
            lastbits += nbits
            if lastbits >= 8:
                lastbits -= 8
                ba[cnt] = (lastbyte >> lastbits) & 0xff
                cnt += 1
        if lastbits > 0:
            ba[cnt] = (lastbyte << (8 - lastbits)) & 0xff
        lastbyte &= 0xff
        for j in range(cnt + 1):
            self.ba[self.cnt + j] = ba[j]
        self.cnt += cnt
        self.lastbyte = lastbyte
        self.lastbits = lastbits

    def sendbyte(self, int nbits, unsigned char  num):
        
        cdef int cnt = 0
        cdef int lastbyte = self.lastbyte
        cdef int lastbits = self.lastbits

        cdef unsigned char[2] ba 
        cdef int j
        if nbits > 0:
            lastbyte = (lastbyte << nbits) | num
            lastbits += nbits
            if lastbits >= 8:
                lastbits -= 8
                ba[cnt] = (lastbyte >> lastbits) & 0xff
                cnt += 1
        if lastbits > 0:
            ba[cnt] = (lastbyte << (8 - lastbits)) & 0xff
        lastbyte &= 0xff
        self.ba[self.cnt] = ba[0]
        if cnt == 1:
            self.ba[self.cnt + 1] = ba[1]
        self.cnt += cnt
        self.lastbyte = lastbyte
        self.lastbits = lastbits

    def rewind(self):
        self.lastbits = 0
        self.lastbyte = 0
        self.cnt = 0
        
    def tobytes(self):
        return bytearray(self.ba[:self.cnt + 1])
    
    def receiveints(self, int bitsize, long[:] sizes):
        cdef int i, j, nbytes, p, num
        cdef int nums[3]
        cdef int ba[32]
        ba[0] = ba[1] = ba[2] = ba[3] = 0
      
        nbytes = 0
        while bitsize > 8:
            ba[nbytes] = self.receiveint(8)
            nbytes += 1
            bitsize -= 8
        if bitsize > 0:
            ba[nbytes] = self.receiveint(bitsize)
            nbytes += 1
        for i in range(2, 0, -1):
            num = 0
            for j in range(nbytes-1, -1, -1):
                num = (num << 8) | ba[j]
                p = num // sizes[i]
                ba[j] = p
                num = num - p * sizes[i]
            nums[i] = num
        nums[0] = ba[0] | (ba[1] << 8) | (ba[2] << 16) | (ba[3] << 24)
        return nums

    def sendints(self, int bitsize, long[:] sizes, int[:] nums):
        cdef unsigned char[32] ba
        cdef int nbytes = 0
        cdef long bignum
        cdef int i
        bignum = (((nums[0] * sizes[1]) + nums[1]) * sizes[2]) + nums[2]

        while bignum > 0:
            ba[nbytes] = bignum & 0xff
            nbytes += 1
            bignum >>= 8
            
        if bitsize >= nbytes * 8:
            for i in range(nbytes):
                self.sendbyte(8, ba[i])
            self.sendbyte(bitsize - nbytes * 8, 0)
        else:
            for i in range(nbytes-1):
                self.sendbyte(8, ba[i])
            self.sendbyte(bitsize - (nbytes-1) * 8, ba[nbytes-1])
    
def unpack_crds(bs, ms, long maxatoms, long natoms, long bitsize, 
                long [:] bitsizeint, long [:] sizes, long [:] minint):
    """
    Unpack a set of coordinates from a BitByteBuffer
    """
    import numpy as np
    
    cdef int run, flag, is_smaller, j, k
    cdef Py_ssize_t i
    
    i = 0
    run = 0
    crds = np.zeros((maxatoms, 3), dtype=np.int)
    cdef long [:,:] crds_v = crds
    
    cdef int smallnum, smallidx
    sizesmall = np.zeros((3), dtype=np.int)
    
    cdef long nums[3]
    cdef long thiscoord[3]
    cdef long prevcoord[3]
    cdef long tmp[3]
    
    cdef long minint0 = minint[0]
    cdef long minint1 = minint[1]
    cdef long minint2 = minint[2]
    
    
    while i < natoms:
        if bitsize == 0:
            thiscoord[0] = bs.receiveint(bitsizeint[0])
            thiscoord[1] = bs.receiveint(bitsizeint[1])
            thiscoord[2] = bs.receiveint(bitsizeint[2])
            
        else:
            thiscoord = bs.receiveints(bitsize, sizes)
        thiscoord[0] += minint0
        thiscoord[1] += minint1
        thiscoord[2] += minint2
        prevcoord = thiscoord

        flag = bs.receiveint(1)
        is_smaller = 0
        if flag == 1:
            run = bs.receiveint(5)
            is_smaller = run % 3
            run -= is_smaller
            is_smaller -= 1
        
        if run > 0:
            smallnum = ms.smallnum
            sizesmall = ms.sizesmall
            smallidx = ms.smallidx
            for k in range(0, run, 3):
                thiscoord = bs.receiveints(smallidx, sizesmall)
                thiscoord[0] += prevcoord[0] - smallnum
                thiscoord[1] += prevcoord[1] - smallnum
                thiscoord[2] += prevcoord[2] - smallnum
                if (k == 0):
                    tmp = thiscoord
                    thiscoord = prevcoord
                    prevcoord = tmp
                    crds_v[i, 0] = prevcoord[0]
                    crds_v[i, 1] = prevcoord[1]
                    crds_v[i, 2] = prevcoord[2]
                    i += 1
                else:
                    prevcoord = thiscoord
                crds_v[i, 0] = thiscoord[0]
                crds_v[i, 1] = thiscoord[1]
                crds_v[i, 2] = thiscoord[2]
                i += 1
        else:
            crds_v[i, 0] = thiscoord[0]
            crds_v[i, 1] = thiscoord[1]
            crds_v[i, 2] = thiscoord[2]
            i += 1
        
        ms.update(is_smaller)

    return crds
