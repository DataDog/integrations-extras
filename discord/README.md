## Overview

Discord is a communication app that lets people connect with each other through text, voice, and video calls. By integrating Datadog with Discord using webhooks you can receive notifications to never miss an important event.

## Setup

1. Follow the [instructions](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) from Discord on how to create a webhook for a channel you want to recieve notifications to.

2. Navigate to the [webhook integration tile](https://app.datadoghq.com/integrations/webhooks) in Datadog and click "New" in the Webhooks section under the Configuration tab.

3. Name your webhook and paste the URL you copied from Discord. Note that you do not need to add an auth-method.

4. You can customize your payload or copy-paste the template below. See the [webhook documentation](https://docs.datadoghq.com/integrations/webhooks/#usage) for more details on available variables.

```json
{
   "embeds":[
      {
         "title":"$EVENT_TITLE",
         "description":"$EVENT_MSG",
         "url":"$LINK",
         "color":"3407966",
         "image":{
            "url":"$SNAPSHOT"
         }
      }
   ]
}
```

## Troubleshooting

Need help? Contact [Datadog support](https://docs.datadoghq.com/help/)