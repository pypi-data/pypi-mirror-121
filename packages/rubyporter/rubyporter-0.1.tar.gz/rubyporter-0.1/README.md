# rubyporter

#### Description
A rpm packager bot for ruby modules from rubygems.org

It is a tool to create spec file and create rpm for ruby modules.
#### Installation

python3 setup.py install

#### Preparation
Install below sofware before using this tool

*  gcc 
*  gdb 
*  libstdc++-devel 
*  ruby-devel
*  rubygems-devel

### Instructions
1. Create spec file, *rubyporter -s xxx*, add *-o xxx* to save to a file
```
e.g.  rubyporter -s puma (generate and display in the screen)
     
      rubyporter -s puma -o rubygem-puma.spec (generate and save to a file)
```


2. Build rpm package, *rubyporter -b xxx*

3. Build and Install rpm package, *rubyporter -B xxx*

4. For more details, please use *rubyporter -h*

#### Contribution
1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request

