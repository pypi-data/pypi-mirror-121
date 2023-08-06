![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)

# PTSAMESITE
> Same Site Scripting Testing Tool

ptsamesite is a tool for testing Same Site Scripting vulnerability. ptsamesite supports mass domain testing.

- Script sends DNS "A" query to domain with 'localhost' as subdomain.
- If DNS responds with IP '127.0.0.1', the record is prone to Same Site Scripting vulnerability. 

## Installation

```
pip install ptsamesite
```

## Usage examples
```
$ ptsamesite -d example.com
$ ptsamesite -d subdomain1.subdomain2.example.com -s
$ ptsamesite -d example.com example2.com
$ ptsamesite -f domain_list.txt
```

## Options
```
-d  --domain      <domain>   Test domain
-f  --file        <file>     Test domains from file
-V  --vulnerable             Print only vulnerable domains
-s  --subdomains             Scan all subdomains of given domain
-t  --threads     <threads>  Number of threads (default 20)
-j  --json                   Output in JSON format
-v  --version                Show script version and exit
-h  --help                   Show this help message and exit
```


## Dependencies
- dnspython
- tldextract
- ptlibs
- ptthreads

## Version History

* 0.0.1 - 0.0.2
    * Alpha releases

## Licence

Copyright (c) 2020 HACKER Consulting s.r.o.

ptsamesite is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ptsamesite is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ptsamesite.  If not, see <https://www.gnu.org/licenses/>.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!