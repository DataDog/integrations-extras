import os

from datadog_checks.base import AgentCheck
from datadog_checks.utils.subprocess_output import get_subprocess_output


class SendmailCheck(AgentCheck):

    def __init__(self, name, init_config, agentConfig, instances=None):
        if instances is not None and len(instances) > 1:
            raise ConfigurationError('Sendmail check only supports one configured instance.')
        AgentCheck.__init__(self, name, init_config, agentConfig, instances=instances)

    def check(self, instance):
        (
            sendmail_directory,
            use_sudo,
            tags,
        ) = self._get_config(instance)

        try:
            queue_size = self._get_sendmail_stats(sendmail_directory, use_sudo)
            self.gauge('sendmail.queue.size', queue_size, tags=tags + ['queue:total'])
            self.log.debug("Sendmail queue size: {} mails".format(queue_size))
        except OSError as e:
            self.log.info("Cannot get sendmail queue info".format(str(e)))
            self.service_check(self.SERVICE_CHECK_NAME,
                               AgentCheck.CRITICAL,
                               tags,
                               message=str(e))

    def _get_config(self, instance):
        sendmail_directory = instance.get('sendmail_directory')
        use_sudo = instance.get('use_sudo', False)
        tags = instance.get('tags', [])

        return (
            sendmail_directory,
            use_sudo,
            tags,
        )

    def _get_sendmail_stats(self, sendmail_directory, use_sudo):

        if not os.path.exists(sendmail_directory):
            raise Exception('{} does not exist'.format(sendmail_directory))

        command = ['ls', sendmail_directory]

        # The mailq command might require sudo access
        if use_sudo:
            test_sudo = os.system('setsid sudo -l < /dev/null')
            if test_sudo != 0:
                raise Exception('The dd-agent user does not have sudo access')
            command.insert(0, 'sudo')

        self.log.info(command)

        files, err, retcode = get_subprocess_output(command, self.log, False)
        if not files:
            file_count = 0
        else:
            self.log.info(sendmail_directory)
            file_count = len(files.split('\n')) - 1
            self.log.info(file_count)

        return file_count
