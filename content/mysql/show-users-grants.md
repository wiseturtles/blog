Title: MySQL查看用户权限
Date: 2014-12-17 11:25
Tags: mysql, user, grants
Slug: show-grants
Author: crazygit
Summary: show mysql user grants


## 命令

SHOW GRANTS

官方文档: <http://dev.mysql.com/doc/refman/5.6/en/show-grants.html>

## 常看帮助

    :::mysql
    mysql> HELP SHOW GRANTS;

## 查看当前登陆用户在当前机器上的权限

    :::mysql
    mysql> SHOW GRANTS;
    mysql> SHOW GRANTS FOR CURRENT_USER;
    mysql> SHOW GRANTS FOR CURRENT_USER();

## 查看特定用户在特定主机上的权限

    :::mysql
    # 查看test用户在主机'%'上的权限(没有指定主机时，默认是'%')
    mysql> SHOW GRANTS FOR 'test';
    # 查看test用户在主机'localhost'上的权限(没有指定主机时，默认是'%')
    mysql> SHOW GRANTS FOR 'test'@'localhost';

## 查看用户在哪些主机上分配了权限

    :::mysql
    mysql> select user,host from mysql.user;


## 各种权限用法表

参考自
<http://dev.mysql.com/doc/refman/5.6/en/grant.html>

<div class="table">
<a name="idm140062991811312"></a><p class="title"><b>Table&nbsp;13.1&nbsp;Permissible Privileges for GRANT and REVOKE</b></p>
<div class="table-contents">
<table summary="Permissible Privileges for GRANT and REVOKE" border="1"><colgroup><col><col></colgroup><thead><tr><th scope="col">Privilege</th><th scope="col">Meaning and Grantable Levels</th></tr></thead><tbody><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_all"><code class="literal">ALL [PRIVILEGES]</code></a></td><td>Grant all privileges at specified access level except
                <a class="link" href="privileges-provided.html#priv_grant-option"><code class="literal">GRANT OPTION</code></a></td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_alter"><code class="literal">ALTER</code></a></td><td>Enable use of <a class="link" href="alter-table.html" title="13.1.7&nbsp;ALTER TABLE Syntax"><code class="literal">ALTER TABLE</code></a>. Levels:
                Global, database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_alter-routine"><code class="literal">ALTER ROUTINE</code></a></td><td>Enable stored routines to be altered or dropped. Levels: Global,
                database, procedure.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create"><code class="literal">CREATE</code></a></td><td>Enable database and table creation. Levels: Global, database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create-routine"><code class="literal">CREATE ROUTINE</code></a></td><td>Enable stored routine creation. Levels: Global, database.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create-tablespace"><code class="literal">CREATE TABLESPACE</code></a></td><td>Enable tablespaces and log file groups to be created, altered, or
                dropped. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create-temporary-tables"><code class="literal">CREATE TEMPORARY TABLES</code></a></td><td>Enable use of <a class="link" href="create-table.html" title="13.1.17&nbsp;CREATE TABLE Syntax"><code class="literal">CREATE
                TEMPORARY TABLE</code></a>. Levels: Global, database.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create-user"><code class="literal">CREATE USER</code></a></td><td>Enable use of <a class="link" href="create-user.html" title="13.7.1.2&nbsp;CREATE USER Syntax"><code class="literal">CREATE USER</code></a>,
                <a class="link" href="drop-user.html" title="13.7.1.3&nbsp;DROP USER Syntax"><code class="literal">DROP USER</code></a>,
                <a class="link" href="rename-user.html" title="13.7.1.5&nbsp;RENAME USER Syntax"><code class="literal">RENAME USER</code></a>, and
                <a class="link" href="revoke.html" title="13.7.1.6&nbsp;REVOKE Syntax"><code class="literal">REVOKE ALL
                PRIVILEGES</code></a>. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_create-view"><code class="literal">CREATE VIEW</code></a></td><td>Enable views to be created or altered. Levels: Global, database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_delete"><code class="literal">DELETE</code></a></td><td>Enable use of <a class="link" href="delete.html" title="13.2.2&nbsp;DELETE Syntax"><code class="literal">DELETE</code></a>. Level: Global,
                database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_drop"><code class="literal">DROP</code></a></td><td>Enable databases, tables, and views to be dropped. Levels: Global,
                database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_event"><code class="literal">EVENT</code></a></td><td>Enable use of events for the Event Scheduler. Levels: Global, database.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_execute"><code class="literal">EXECUTE</code></a></td><td>Enable the user to execute stored routines. Levels: Global, database,
                table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_file"><code class="literal">FILE</code></a></td><td>Enable the user to cause the server to read or write files. Level:
                Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_grant-option"><code class="literal">GRANT OPTION</code></a></td><td>Enable privileges to be granted to or removed from other accounts.
                Levels: Global, database, table, procedure, proxy.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_index"><code class="literal">INDEX</code></a></td><td>Enable indexes to be created or dropped. Levels: Global, database,
                table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_insert"><code class="literal">INSERT</code></a></td><td>Enable use of <a class="link" href="insert.html" title="13.2.5&nbsp;INSERT Syntax"><code class="literal">INSERT</code></a>. Levels: Global,
                database, table, column.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_lock-tables"><code class="literal">LOCK TABLES</code></a></td><td>Enable use of <a class="link" href="lock-tables.html" title="13.3.5&nbsp;LOCK TABLES and UNLOCK TABLES Syntax"><code class="literal">LOCK TABLES</code></a> on tables for
                which you have the <a class="link" href="select.html" title="13.2.9&nbsp;SELECT Syntax"><code class="literal">SELECT</code></a>
                privilege. Levels: Global, database.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_process"><code class="literal">PROCESS</code></a></td><td>Enable the user to see all processes with <a class="link" href="show-processlist.html" title="13.7.5.30&nbsp;SHOW PROCESSLIST Syntax"><code class="literal">SHOW
                PROCESSLIST</code></a>. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_proxy"><code class="literal">PROXY</code></a></td><td>Enable user proxying. Level: From user to user.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_references"><code class="literal">REFERENCES</code></a></td><td>Not implemented</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_reload"><code class="literal">RELOAD</code></a></td><td>Enable use of <a class="link" href="flush.html" title="13.7.6.3&nbsp;FLUSH Syntax"><code class="literal">FLUSH</code></a> operations. Level:
                Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_replication-client"><code class="literal">REPLICATION CLIENT</code></a></td><td>Enable the user to ask where master or slave servers are. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_replication-slave"><code class="literal">REPLICATION SLAVE</code></a></td><td>Enable replication slaves to read binary log events from the master.
                Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_select"><code class="literal">SELECT</code></a></td><td>Enable use of <a class="link" href="select.html" title="13.2.9&nbsp;SELECT Syntax"><code class="literal">SELECT</code></a>. Levels: Global,
                database, table, column.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_show-databases"><code class="literal">SHOW DATABASES</code></a></td><td>Enable <a class="link" href="show-databases.html" title="13.7.5.15&nbsp;SHOW DATABASES Syntax"><code class="literal">SHOW DATABASES</code></a> to show all
                databases. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_show-view"><code class="literal">SHOW VIEW</code></a></td><td>Enable use of <a class="link" href="show-create-view.html" title="13.7.5.14&nbsp;SHOW CREATE VIEW Syntax"><code class="literal">SHOW CREATE VIEW</code></a>. Levels:
                Global, database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_shutdown"><code class="literal">SHUTDOWN</code></a></td><td>Enable use of <a class="link" href="mysqladmin.html" title="4.5.2&nbsp;mysqladmin — Client for Administering a MySQL Server"><span class="command"><strong>mysqladmin shutdown</strong></span></a>. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_super"><code class="literal">SUPER</code></a></td><td>Enable use of other administrative operations such as
                <a class="link" href="change-master-to.html" title="13.4.2.1&nbsp;CHANGE MASTER TO Syntax"><code class="literal">CHANGE MASTER TO</code></a>,
                <a class="link" href="kill.html" title="13.7.6.4&nbsp;KILL Syntax"><code class="literal">KILL</code></a>,
                <a class="link" href="purge-binary-logs.html" title="13.4.1.1&nbsp;PURGE BINARY LOGS Syntax"><code class="literal">PURGE BINARY LOGS</code></a>,
                <a class="link" href="set-statement.html" title="13.7.4&nbsp;SET Syntax"><code class="literal">SET
                GLOBAL</code></a>, and <a class="link" href="mysqladmin.html" title="4.5.2&nbsp;mysqladmin — Client for Administering a MySQL Server"><span class="command"><strong>mysqladmin
                debug</strong></span></a> command. Level: Global.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_trigger"><code class="literal">TRIGGER</code></a></td><td>Enable trigger operations. Levels: Global, database, table.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_update"><code class="literal">UPDATE</code></a></td><td>Enable use of <a class="link" href="update.html" title="13.2.11&nbsp;UPDATE Syntax"><code class="literal">UPDATE</code></a>. Levels: Global,
database, table, column.</td></tr><tr><td scope="row"><a class="link" href="privileges-provided.html#priv_usage"><code class="literal">USAGE</code></a></td><td>Synonym for <span class="quote">“<span class="quote">no privileges</span>”</span></td></tr></tbody></table>
</div>

</div>
