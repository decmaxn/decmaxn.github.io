# Git_controlled_doc_on_confluence


# Why
Git can be used for managing changes to other types of files, such as documents. For documents related to code and infra, Confluence can be just a publshing system, while the Version tracking, Collaboration, Branching and Backup happens at Git side. 

There should be a CICD pipeline to deploy changes to Confluence.

# Instruction
[Confluence Publisher](https://confluence-publisher.atlassian.net/wiki/spaces/CPD/overview?mode=global) can be used for this purpose. Refer to it's  [Github](https://github.com/confluence-publisher/confluence-publisher.git)  for details. 

Also [Docker Image](https://hub.docker.com/r/confluencepublisher/confluence-publisher) seems to be updated recently as well.

```bash
docker pull confluencepublisher/confluence-publisher:0.0.0-SNAPSHOT

export BUILD_SOURCESDIRECTORY=$(pwd)
export ROOT_CONFLUENCE_URL=https://hotmailbox.atlassian.net/wiki/home
export USERNAME=hotmailbox@hotmail.com
export PASSWORD=<tobereplaced>
export SPACE_KEY=<to be replaced>
export ANCESTOR_ID=327681
export PUBLISHING_STRATEGY=APPEND_TO_ANCESTOR  

docker run --rm -v $BUILD_SOURCESDIRECTORY/$CONSOLIDATED_FOLDER_NAME/docs/:/var/asciidoc-root-folder -e ROOT_CONFLUENCE_URL=$ROOT_CONFLUENCE_URL \
  -e SKIP_SSL_VERIFICATION=false \
  -e USERNAME=$USERNAME \
  -e PASSWORD=$PASSWORD \
  -e SPACE_KEY=$SPACE_KEY \
  -e ANCESTOR_ID=$GITHUB_ANCESTOR_ID \
  -e PUBLISHING_STRATEGY=$PUBLISHING_STRATEGY \
  confluencepublisher/confluence-publisher:0.0.0-SNAPSHOT
```
# Details

If you are registered as Confluence with microsoft or gmail account, the USERNAME and PASSWORD are your email address and email password. Also replace hotmailbox above with your mailbox name.

SPACE_KEY can be found at at Confluence "space settings" page and "Space details" link.

ANCESTOR_ID is the parent page's ID, can be founded in the URL after /pages/when you open that page. etc. 327681
https://hotmailbox.atlassian.net/wiki/spaces/~xxxxxxxxxx/pages/327681/Manually+created+Doc-+Test

For PUBLISHING_STRATEGY I can only find APPEND_TO_ANCESTOR. 


# Troubleshooting

Trying to fix the following error, I found out details above.

```
in thread "main" java.lang.IllegalArgumentException: No enum constant org.sahli.asciidoc.confluence.publisher.client.PublishingStrategy.UPDATE


in thread "main" java.lang.IllegalArgumentException: No enum constant org.sahli.asciidoc.confluence.publisher.client.PublishingStrategy.UPDATE_OR_CREATE


in thread "main" java.lang.IllegalArgumentException: No root page found, but 'REPLACE_ANCESTOR' publishing strategy requires one single root page

in thread "main" java.lang.IllegalArgumentException: No enum constant org.sahli.asciidoc.confluence.publisher.client.PublishingStrategy.APPEND_ANCESTOR

in thread "main" org.sahli.asciidoc.confluence.publisher.client.http.RequestFailedException: request failed response: 401 Unauthorized Basic authentication with passwords is deprecated.  For more information, see: https://developer.atlassian.com/cloud/confluence/deprecation-notice-basic-auth/, reason: <none>)
```
But the last error lead me to the following error.
> The deprecation period for this functionality has ended. From June 3rd, 2019, we will be progressively disabling the usage of this authentication method.

> If you are using a REST endpoint in Confluence with basic authentication, update your app or integration to use API tokens, OAuth, or Atlassian Connect.

# Conclusion

The purpose of this test is to prove the idea, although the tool seems be outdated, I believe is archieved. 
