#!/usr/bin/env python3

# Copyright (c) 2021, harens
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the documentation
#       and/or other materials provided with the distribution.
#     * Neither the name of seaport nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# TODO: Sort out if online, if offline
# TODO: Allow for other repositories (not just MacPorts)
# TODO: Test docstrings

from depythel.macports.online import retrieve_deps

from typing import NamedTuple, Optional
from collections import deque

class Dependency(NamedTuple):
  """A named tuple representing dependency nodes in the tree.
  
  Examples:
    >>> from depythel.main import Dependency
    >>> # The main root dependency
    >>> Dependency('gping', 0, 'Root', 0, None)
    Dependency(name='gping', id=0, info='Root', level=0, parent=None)
    >>> # 1 level down child dependency
    >>> Dependency('clang-12', 1, 'Buildtime', 1, 'gping')
    Dependency(name='clang-12', id=1, info='Buildtime', level=1, parent='gping')
  """
  name: str
  """The name of the main root dependency. The dependency tree is generated from this."""
  
  id: int
  """A unique id for the dependency in the tree. Starts at 0."""
  
  info: str
  """Information about the port, such as whether it is a buildtime/runtime dependency."""
  
  level: int
  """How many levels down a dependency is in the dependency tree."""
  
  parent: Optional[int]
  """Which project requires this dependency (its parent)."""


if __name__ == "__main__":
  queue = deque(Dependency(root_dep, 0, "root", 0, None))
