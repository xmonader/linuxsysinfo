#!/usr/bin/env python
#  sysinfo.py
#
#  Copyright 2016 ahmed t. youssef <xmonader at gmail dot com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from ctypes import *

libc=None
try:
    libc=CDLL("libc.so.6")
except ImportError:
    print("libc.so is not found.")
    exit(1)



"""
//AT /usr/include/linux/sysinfo.h

#ifndef _LINUX_SYSINFO_H
#define _LINUX_SYSINFO_H

#include <linux/types.h>

#define SI_LOAD_SHIFT   16
struct sysinfo {
    __kernel_long_t uptime;     /* Seconds since boot */
    __kernel_ulong_t loads[3];  /* 1, 5, and 15 minute load averages */
    __kernel_ulong_t totalram;  /* Total usable main memory size */
    __kernel_ulong_t freeram;   /* Available memory size */
    __kernel_ulong_t sharedram; /* Amount of shared memory */
    __kernel_ulong_t bufferram; /* Memory used by buffers */
    __kernel_ulong_t totalswap; /* Total swap space size */
    __kernel_ulong_t freeswap;  /* swap space still available */
    __u16 procs;            /* Number of current processes */
    __u16 pad;          /* Explicit padding for m68k */
    __kernel_ulong_t totalhigh; /* Total high memory size */
    __kernel_ulong_t freehigh;  /* Available high memory size */
    __u32 mem_unit;         /* Memory unit size in bytes */
    char _f[20-2*sizeof(__kernel_ulong_t)-sizeof(__u32)];   /* Padding: libc5 uses this.. */
};

#endif /* _LINUX_SYSINFO_H */


//AT /usr/include/sys/sysinfo.h
/* Returns information on overall system statistics.  */
extern int sysinfo (struct sysinfo *__info) __THROW;


/* Return number of configured processors.  */
extern int get_nprocs_conf (void) __THROW;

/* Return number of available processors.  */
extern int get_nprocs (void) __THROW;


/* Return number of physical pages of memory in the system.  */
extern long int get_phys_pages (void) __THROW;

/* Return number of available physical pages of memory in the system.  */
extern long int get_avphys_pages (void) __THROW;


"""


#sysinfo structure: /usr/include/linux/sysinfo.h
class sysinfo_s(Structure):
    _fields_=[
        ('uptime', c_long),
        ('totalram', c_ulong),
        ('freeram', c_ulong),
        ('sharedram', c_ulong),
        ('bufferram', c_ulong),
        ('totalswap', c_ulong),
        ('freeswap', c_ulong),
        ('totalhigh', c_ulong),
        ('freehigh', c_ulong),
        ('loads', c_ulong*3),
        ('procs', c_uint),
        ('pad', c_uint),
        ('mem_unit', c_uint),

    ]


#sysinfo signature: /usr/include/sys/sysinfo.h
sysinfo=libc.sysinfo
sysinfo.restype=c_int
sysinfo.argtypes =[POINTER(sysinfo_s)]


def get_sysinfo():
    info_s = sysinfo_s()
    res = sysinfo(byref(info_s))
    if res == 0: # not sure if there's error=-1 specified for that function, but it returns an int
        return info_s

if __name__=="__main__":
    info_s = get_sysinfo()
    if info_s is not None:
        for attr, t_ in info_s._fields_:
            attrval=getattr(info_s, attr)
            print("%s => %s"%(attr, str(attrval)))
    else:
            print("Error processing sysinfo")

