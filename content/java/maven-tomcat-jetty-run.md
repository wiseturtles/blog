Title: Maven通过plugin在Tomcat、Jetty中运行项目
Date: 2016-02-09 16:00
Tags: Java,Maven,Tomcat,Jetty
Slug: maven-plugin-tomcat-jetty-run
Author: ox0spy
Summary: Maven通过plugin在Tomcat、Jetty中运行项目


记录下如何在pom.xml中配置插件，通过tomcat、Jetty运行项目.

## 配置pom.xml

```
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.tomcat.maven</groupId>
            <artifactId>tomcat6-maven-plugin</artifactId>
            <version>2.2</version>
        </plugin>

        <plugin>
            <groupId>org.apache.tomcat.maven</groupId>
            <artifactId>tomcat7-maven-plugin</artifactId>
            <version>2.2</version>
        </plugin>

        <plugin>
            <groupId>org.mortbay.jetty</groupId>
            <artifactId>jetty-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

## 测试

### Maven Tomcat plugin

    :::bash
    $ mvn tomcat:run
    $ mvn tomcat7:run

### Maven Jetty plugin
    :::bash
    $ mvn jetty:run
