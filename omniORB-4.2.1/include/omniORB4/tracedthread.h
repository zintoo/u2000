// -*- Mode: C++; -*-
//                            Package   : omniORB2
// tracedthread.h             Created on: 15/6/99
//                            Author    : David Riddoch (djr)
//
//    Copyright (C) 2010-2013 Apasphere Ltd
//    Copyright (C) 1996-1999 AT&T Research Cambridge
//
//    This file is part of the omniORB library.
//
//    The omniORB library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Library General Public
//    License as published by the Free Software Foundation; either
//    version 2 of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    Library General Public License for more details.
//
//    You should have received a copy of the GNU Library General Public
//    License along with this library; if not, write to the Free
//    Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
//    02111-1307, USA
//
//
// Description:
//    omni_thread style mutex and condition variables with checks.
//

#ifndef __OMNI_TRACEDTHREAD_H__
#define __OMNI_TRACEDTHREAD_H__


// Lock tracing is controlled by autoconf, or in the dummy
// omniconfig.h.  You can override it here if you wish.

//#define OMNIORB_ENABLE_LOCK_TRACES


//////////////////////////////////////////////////////////////////////
////////////////////////// omni_tracedmutex //////////////////////////
//////////////////////////////////////////////////////////////////////

#ifndef OMNIORB_ENABLE_LOCK_TRACES

#define ASSERT_OMNI_TRACEDMUTEX_HELD(m, yes)

class omni_tracedmutex : public omni_mutex {
public:
  inline omni_tracedmutex(const char* /*name*/=0) : omni_mutex() {}
};

typedef omni_mutex_lock omni_tracedmutex_lock;

class omni_tracedcondition : public omni_condition {
public:
  inline omni_tracedcondition(omni_tracedmutex* m, const char* /*name*/=0)
    : omni_condition(m) {}
};

#else

class omni_tracedcondition;


class omni_tracedmutex {
public:
  omni_tracedmutex(const char* name=0);
  ~omni_tracedmutex();

  void lock();
  void unlock();
  inline void acquire(void) { lock();   }
  inline void release(void) { unlock(); }

  void assert_held(const char* file, int line, int yes);

private:
  friend class omni_tracedcondition;

  omni_tracedmutex(const omni_tracedmutex&);
  omni_tracedmutex& operator=(const omni_tracedmutex&);

  omni_mutex     pd_lock;    // protects other members
  omni_condition pd_cond;    // so can wait for mutex to unlock
  omni_thread*   pd_holder;  // the thread holding pd_m, or 0
  int            pd_n_conds; // number of dependent condition vars
  int            pd_deleted; // set true on deletion, may catch later use
  char*          pd_logname; // name to use for logging
};

//////////////////////////////////////////////////////////////////////
//////////////////////// omni_tracedcondition ////////////////////////
//////////////////////////////////////////////////////////////////////

class omni_tracedcondition {
public:
  omni_tracedcondition(omni_tracedmutex* m, const char* name = 0);
  ~omni_tracedcondition();

  void wait();
  int timedwait(unsigned long secs, unsigned long nanosecs = 0);
  inline int timedwait(const omni_time_t& t) { return timedwait(t.s, t.ns); }
  void signal();
  void broadcast();

private:
  omni_tracedcondition(const omni_tracedcondition&);
  omni_tracedcondition& operator=(const omni_tracedcondition&);

  omni_tracedmutex& pd_mutex;
  omni_condition    pd_cond;
  int               pd_n_waiters;
  int               pd_deleted;
  char*             pd_logname;
};

//////////////////////////////////////////////////////////////////////
//////////////////////// omni_tracedmutex_lock ///////////////////////
//////////////////////////////////////////////////////////////////////

class omni_tracedmutex_lock {
public:
  inline omni_tracedmutex_lock(omni_tracedmutex& m) :pd_m(m) { m.lock(); }
  inline ~omni_tracedmutex_lock() { pd_m.unlock(); }

private:
  omni_tracedmutex_lock(const omni_tracedmutex_lock&);
  omni_tracedmutex_lock& operator = (const omni_tracedmutex_lock&);

  omni_tracedmutex& pd_m;
};


#define ASSERT_OMNI_TRACEDMUTEX_HELD(m, yes)  \
  (m).assert_held(__FILE__, __LINE__, (yes))

// #ifndef OMNIORB_ENABLE_LOCK_TRACES
#endif


//////////////////////////////////////////////////////////////////////
///////////////////////// omni_optional_lock /////////////////////////
//////////////////////////////////////////////////////////////////////

class omni_optional_lock {
public:
  inline omni_optional_lock(omni_tracedmutex& m, int locked,
			    int locked_on_exit)
    : pd_locked(locked_on_exit), pd_m(m)
    { if( !locked ) pd_m.lock(); }

  inline ~omni_optional_lock() { if( !pd_locked )  pd_m.unlock(); }

private:
  omni_optional_lock(const omni_optional_lock&);
  omni_optional_lock& operator = (const omni_optional_lock&);

  int               pd_locked;
  omni_tracedmutex& pd_m;
};


//////////////////////////////////////////////////////////////////////
//////////////////////// omni_tracedmutex_unlock /////////////////////
//////////////////////////////////////////////////////////////////////

class omni_tracedmutex_unlock {
public:
  inline omni_tracedmutex_unlock(omni_tracedmutex& m) : pd_m(m) { m.unlock(); }
  inline ~omni_tracedmutex_unlock() { pd_m.lock(); }

private:
  omni_tracedmutex_unlock(const omni_tracedmutex_unlock&);
  omni_tracedmutex_unlock& operator=(const omni_tracedmutex_unlock&);

  omni_tracedmutex& pd_m;
};


#endif  // __OMNITRACEDTHREAD_H__
