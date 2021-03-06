#!/usr/bin/env bash

################################################################################
# CruiseControl, a Continuous Integration Toolkit
# Copyright (c) 2001, ThoughtWorks, Inc.
# 200 E. Randolph, 25th Floor
# Chicago, IL 60601 USA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     + Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     + Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     + Neither the name of ThoughtWorks, Inc., CruiseControl, nor the
#       names of its contributors may be used to endorse or promote
#       products derived from this software without specific prior
#       written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

# CCDIR: The root of the CruiseControl directory.
# The key requirement is that this is the parent
# directory of CruiseControl's lib and dist directories.
if [ -z "$CCDIR" ] ; then
  # resolve links - $0 may be a softlink
  PRG="$0"

  # need this for relative symlinks
  while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \(.*\)$'`
    if expr "$link" : '/.*' > /dev/null; then
      PRG="$link"
    else
      PRG=`dirname "$PRG"`"/$link"
    fi
  done

  saveddir=`pwd`

  CCDIR=`dirname "$PRG"`

  # make it fully qualified
  CCDIR=`cd "$CCDIR" && pwd`

  cd $saveddir
  echo Using Cruise Control at $CCDIR
fi

# Uncomment the following line if you have OutOfMemoryError errors
# CC_OPTS="-Xms128m -Xmx256m"

#--------------------------------------------
# set JAVA_HOME on Mac OSX
#--------------------------------------------
case "`uname`" in
  Darwin*)
    if [ -z "$JAVA_HOME" ] ; then
      JAVA_HOME=/System/Library/Frameworks/JavaVM.framework/Home
    fi
    ;;
esac

LIBDIR=$CCDIR/lib
LAUNCHER=$LIBDIR/cruisecontrol-launcher.jar
if [ -z "$JETTY_LOGS" ] ; then 
 JETTY_LOGS=$CCDIR/logs 
fi 

if [ `uname | grep -n CYGWIN` ]; then
 JETTY_LOGS=`cygpath --windows "$JETTY_LOGS"`
fi

# convert the existing path to unix
if [ `uname | grep -n CYGWIN` ]; then
   JAVA_HOME=`cygpath --path --unix "$JAVA_HOME"`
fi

# convert the existing path to unix
if [ `uname | grep -n CYGWIN` ]; then
  CRUISE_PATH=`cygpath --path --windows "$CRUISE_PATH"`
fi

if [ `uname | grep -n CYGWIN` ]; then
  LAUNCHER=`cygpath --windows "$LAUNCHER"`
fi

EXEC="$JAVA_HOME/bin/java $CC_OPTS -Djavax.management.builder.initial=mx4j.server.MX4JMBeanServerBuilder -Dcc.library.dir=$LIBDIR -Djetty.logs=$JETTY_LOGS -jar $LAUNCHER $@ -jmxport 8000 -webport 8080 -rmiport 1099"
echo $EXEC
$JAVA_HOME/bin/java $CC_OPTS -Djavax.management.builder.initial=mx4j.server.MX4JMBeanServerBuilder "-Dcc.library.dir=$LIBDIR" "-Djetty.logs=$JETTY_LOGS" -jar "$LAUNCHER" $@ -jmxport 8000 -webport 8080 -rmiport 1099 &
echo $! > cc.pid
