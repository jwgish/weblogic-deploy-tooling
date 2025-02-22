### Specifying RCU connection information in the model

During creating or updating a domain, there is new section `RCUDbInfo` in the model, under the `domainInfo` section, for specifying RCU database connection information without using the command-line arguments `-rcu_db` and `-rcu_prefix`. Use this to support a database where the connection string is more complex and requires extra options.

### Access a database using a wallet

When accessing a database using a wallet, you need to obtain the wallet from your DBA and information about the database:

- `tns alias` - The network service name. You can find this in the `tnsnames.ora` file inside the database wallet.  The alias is on the left side of the equals sign.

   ```text
   xxxx = (DESCRIPTION ...)
   yyyy = (DESCRIPTION ...)
   ...
   ```

- `keystore and truststore password` - Password used to generate the wallet.
- `keystore and truststore type` - SSO or PKCS12.
- `keystore and truststore file` - `cwallet.sso` (if store type is SSO), `ewallet.p12` (if store type is PKCS12).

Depending on the type of database and the choice of method for authentication, you can provide the necessary information with `RCUDbInfo` in the model.

#### ATP database

For example, to use the Oracle Autonomous Transaction Processing Cloud Database for a JRF domain, specify the following information in the model:

```yaml
domainInfo:
    RCUDbInfo:
        useATP : true
        rcu_prefix : DEV
        rcu_admin_password: <database admin password is required only when you specify -run_rcu flag>
        rcu_schema_password : <RCU schema password>
        atp.admin.user : admin
        tns.alias : <tns alias name. e.g. dbname_tp>
        javax.net.ssl.keyStorePassword : <atp wallet password when generating the wallet from Oracle Cloud Console>
        javax.net.ssl.trustStorePassword : <atp wallet password when generating the wallet from Oracle Cloud Console>
        oracle.net.tns_admin: <optional: absolute path of the unzipped wallet root directory (outside of the archive), if the wallet.zip is not included in the archive>
```
The database wallet can be included in the archive file under `atpwallet` zipentry structure

`atpwallet/Walletxyz.zip`

Or, by specifying the unzipped root directory of the ATP wallet ZIP file in `oracle.net.tns_admin`.

**Note: Prior to release 0.23, the `useATP` flag only accepts values of `0`, `1`, `true`, or `false`.**

#### SSL database using SSO for authentication

For an SSL database, with an `SSO` wallet, use the following example:
```yaml
domainInfo:
    RCUDbInfo:
      useSSL : true
      rcu_db_conn_string: <reuired URL string for use with -run_rcu>
      rcu_prefix : DEV
      rcu_admin_password: <required with -run_rcu flag>
      rcu_schema_password: <required with -run_rcu flag>
      tns.alias: <alias of ssl db in the tnsnames.ora file>
      javax.net.ssl.keyStore: <keystore found in unzipped wallet, i.e. cwallet.sso>
      javax.net.ssl.keyStoreType: SSO
      javax.net,ssl.trustStore: <truststore found in unzipped wallet, i.e cwallet.sso>
      javax.net.ssl.trustStoreType: SSO
      oracle.net.tns_admin: <absolute path of the unzipped wallet root directory>

```
#### SSL database using PKCS12 for authentication

For an SSL database, with a `PKCS12` wallet, use the following example:
```yaml
domainInfo:
    RCUDbInfo:
      useSSL : true
      rcu_db_conn_string: <reuired URL string for use with -run_rcu>
      rcu_prefix : DEV
      rcu_admin_password: <required with -run_rcu flag>
      rcu_schema_password: <required with -run_rcu flag>
      tns.alias: <alias of ssl db in the tnsnames.ora file>
      javax.net.ssl.keyStore: <keystore found in the unzipped wallet, i.e. ewallet.p12>
      javax.net.ssl.keyStoreType: PKCS12
      javax.net.ssl.keyStorePassword: <keystore password>
      javax.net.ssl.trustStore: <truststore found in the unzipped wallet, i.e ewallet.p12>
      javax.net.ssl.trustStoreType: PKCS12
      javax.net.ssl.trustStorePassword: <password of the truststore>
      oracle.net.tns_admin: <absolute path of the unzipped wallet root directory>

```
When using a PKCS12 wallet, you must include the Oracle PKI provider to access your wallet. Add the Oracle PKI provider to your Java `java.security` file. For more information, see Section 2.2.4 "How can Oracle wallets be used in Java" in [SSL with Oracle JDBC Thin Driver](https://www.oracle.com/technetwork/topics/wp-oracle-jdbc-thin-ssl-130128.pdf).

### Access a database without using a wallet (non wallet-based access)

For a typical database, use the following example:

```yaml
domainInfo:
    RCUDbInfo:
        rcu_prefix : DEV
        # Optional rcu_db_user for creating RCU schema if -run_rcu flag is specified. Default user is SYS if not specified.
        # This user must have SYSDBA privilege and this is the equivalent of -dbUser in the RCU utility.
        rcu_db_user: superuser
        rcu_schema_password : <rcu schema password, will be prompted if not specified>
        rcu_admin_password : <database admin password is required only when you specify -run_rcu flag, will be prompted
         if not specified>
        rcu_db_conn_string : dbhost:1521/pdborcl
```        

### Specify variables for RCU

RCU `-variables` option of the repository creation utility can now be included in the `RCUDbInfo` section with the key `rcu_variables`:

```yaml
domainInfo:
    RCUDbInfo:
        rcu_variables : xxxx
```    

### Specify extended XML files for RCU

When creating a domain using WDT and the `-run_rcu` option, you can specify your extended XML files in the `RCUDbInfo` section.

This correlates to the `createRepository` and `dropRepository` command-line arguments `RCU -compInfoXMLLocation <file path> -storageXMLLocation <file path>`.

Include your XML files in your archive file using the location `wlsdeploy/rcu/config`. Then include this relative location in the `RCUDbInfo` section of the model.

```yaml
domainInfo:
    RCUDbInfo:
        compInfoXMLLocation: wlsdeploy/rcu/config/MyComponentInfo.xml
        storageXMLLocation: wlsdeploy/rcu/config/MyStorage.xml
```
