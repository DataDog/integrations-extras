import os

from datadog_checks.base import AgentCheck, ConfigurationError, is_affirmative
from datadog_checks.base.utils.subprocess_output import get_subprocess_output


class SendmailCheck(AgentCheck):

    SERVICE_CHECK_NAME = 'sendmail.returns.output'

    def check(self, instance):
        (sendmail_command, use_sudo, tags) = self._get_config(instance)

        if not sendmail_command:
            raise ConfigurationError('Please provide the sendmail command in the configuration')

        valid_commands = ["mailq", "sendmail"]

        if not any(cmd in sendmail_command for cmd in valid_commands):
            raise ConfigurationError("{} does not seem to be a valid command".format(sendmail_command))

        try:
            queue_size = self._get_sendmail_stats(sendmail_command, use_sudo)
            self.gauge('sendmail.queue.size', queue_size, tags=tags + ['queue:total'])
            self.log.debug("Sendmail queue size: %s mails", queue_size)
            # Send an OK service check as well
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK, tags)
        except OSError as e:
            self.log.info("Cannot get sendmail queue info: %s", e)
            self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.CRITICAL, tags, message=str(e))

    def _get_config(self, instance):
        sendmail_command = instance.get('sendmail_command')
        use_sudo = is_affirmative(instance.get('use_sudo', False))
        tags = instance.get('tags', [])

        return sendmail_command, use_sudo, tags

    def _get_sendmail_stats(self, sendmail_command, use_sudo):

        if not os.path.exists(sendmail_command):
            raise Exception('{} does not exist'.format(sendmail_command))

        self.log.debug(sendmail_command)

        # mailq sample output. sendmail output is similar.
        ##
        # MSP Queue status...
        # /var/spool/mqueue-client is empty
        #    Total requests: 0
        # MTA Queue status...
        # /var/spool/mqueue is empty
        #     Total requests: 0

        # if we want to use sendmail, we need to append -bp to it
        # https://www.electrictoolbox.com/show-sendmail-mail-queue/
        if "sendmail" in sendmail_command:
            command = [sendmail_command, '-bp']
        else:
            command = [sendmail_command]

        # Listing the directory might require sudo privileges
        if use_sudo:
            try:
                os.system('setsid sudo -l < /dev/null')
                command.insert(0, 'sudo')
            except OSError as e:
                self.log.exception("trying to retrieve %s with sudo failed with return code %s", command, e)

        self.log.debug(command)

        mail_queue, err, retcode = get_subprocess_output(command, self.log, False)
        self.log.debug("Error: %s", err)
        count = mail_queue.splitlines()
        # Retrieve the last total number of requests
        queue_count = int(count[-1][-1])
        self.log.info("Number of mails in the queue: %s", queue_count)

        return queue_count
