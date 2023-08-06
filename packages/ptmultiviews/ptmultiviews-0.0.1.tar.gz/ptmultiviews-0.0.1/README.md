![penterepTools](https://www.penterep.com/external/penterepToolsLogo.png)


# ptmultiviews
> Apache Multiviews Detection & Enumeration Tool

ptmultiviews is a tool that detects if supplied web application is vulnerable to Apache Multiviews. If so, script enumerates all alternatives for accessed file. Script can load a list of files for mass enumeration.

## Installation

```
pip install ptmultiviews
```

## Add to PATH
```bash
# If you cannot invoke the script in your terminal, its probably because its not in your PATH. Fix it by running commands below.
echo "export PATH=\"`python3 -m site --user-base`/bin:\$PATH\"" >> ~/.bashrc
source ~/.bashrc
```

## Usage examples

```
ptmultiviews -u https://www.example.com/                          # Test single URL for MultiViews vulnerability and retrieve alternatives
ptmultiviews -u https://www.example.com/ -co                      # Test single URL for MultiViews vulnerability without enumeration
ptmultiviews -u https://www.example.com/index.php -wr             # Prints enumerated files without requested url
ptmultiviews -u https://www.example.com/index.php -wd             # Prints enumerated files without domain part
ptmultiviews -u https://www.example.com/index.php -o output.txt   # Saves enumerated files to output.txt 
```

### Options:

```
   -u   --url         <url>           Connect to URL
   -d   --domain      <domain>        Domain to test, (use with --file argument)
   -f   --file        <file>          Load list of URLs from file
   -co  --check-only                  Check for multiviews without enumerating
   -o   --output      <output>        Save output to file
   -wr  --without-requested-url       Enumerated files will be printed without the requested url
   -wd  --without-domain              Enumerated files will be printed without domain
   -r   --redirect                    Follow redirects (default False)
   -t   --threads     <threads>       Set number of threads (default 20)
   -p   --proxy       <proxy>         Set proxy (e.g. 127.0.0.1:8080)
   -ua  --user-agent  <ua>            Set User-Agent header
   -H   --headers     <header:value>  Use custom headers
   -c   --cookie      <cookie>        Set cookie
   -j   --json                        Output in JSON format
   -v   --version                     Show script version and exit
   -h   --help                        Show this help message and exit
```

## Dependencies

```
requests
ptlibs
ptthreads
```

## Version History

    0.0.1
        Alpha release

## License

Copyright (c) 2020 HACKER Consulting s.r.o.

ptmultiviews is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

ptmultiviews is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ptmultiviews. If not, see https://www.gnu.org/licenses/.

## Warning

You are only allowed to run the tool against the websites which
you have been given permission to pentest. We do not accept any
responsibility for any damage/harm that this application causes to your
computer, or your network. Penterep is not responsible for any illegal
or malicious use of this code. Be Ethical!
