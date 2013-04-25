## SublimeSalesforce Features
* Salesforce Deployment With ST2 Build System + Apache Ant
* Anonymous Code Execution
* Working Syntax Highlighter ( Thanks for especially sucking on this one Force.com IDE )


## Setup
### Pre-requisites
#### Build Tool/Deployment
* Java JDK ( http://java.sun.com/javase/downloads/index.jsp )
* Apache Ant ( http://ant.apache.org/ )
* Force.com Migration Tool ( http://www.salesforce.com/us/developer/docs/apexcode/Content/apex_deploying_ant.htm )

### Salesforce Setup
For Ant deployment you will be required to maintain three files, package.xml, build.xml, and build.properties.
For our dev stack these files are used by continuous integration scripts. So rather than trying to have each dev
modify these files we opted for everyone to instead maintain their own local (local-build.xml, local-build.properties)
versions of these files. These are the files targeted by the build system in this package.

TL;DR

You will need to have the following three files in the project directory for the build system to work:

local-build.properties - ex.

```
# build.properties
# My Sandbox
sf.username = mysalesforcename@mydomain.com.sandboxname
sf.password = mysalesforcepassword
sf.serverurl = https://test.salesforce.com
```

local-build.xml - ex.
```
<target name="deployCode">
 <sf:deploy username="${sf.username}" password="${sf.password}" serverurl="${sf.serverurl}" deployRoot="src">
  <runTest>TestClassToRun</runTest>
  <runTest>AnotherOne</runTest>
 </sf:deploy>
</target>
```

package.xml - ex.
```
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>TestClassToRun</member>
    	<members>AnotherOne</member>
		<name>ApexClass</name>
    </types>
    <types>
        <members>SomeTrigger</members>
        <name>ApexTrigger</name>
    </types>
    <types>
        <members>Lead.CleanPhone__c</members>
        <name>CustomField</name>
    </types>
    <types>
        <members>My_Custom_Object__c</members>
        <name>CustomObject</name>
    </types>
    <version>27.0</version>
</Package>
```

Refer to Salesforce documentation for any questions/further information about these files.

### Sublime Package Setup
```
$ cd your_st2_directory/Packages
$ git clone git://github.com/systemsoverload/SublimeSalesforce.git
```

### Todo
* Schema Explorer
* Clean-up 'Execute Anonymous'
