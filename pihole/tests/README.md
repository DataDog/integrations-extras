Note:

etc-dnsmasq.d & etc-pihole are required for spinning up a pihole container.
These folders are taken at runtime from your local system during container creation - ususally.

Due to permission issues, I have included the basics with the correct permissions and modified the volume mounts in docker-compose.yaml accordingly.

The time.sleep in conftest.py is used as the test cant be correctly yielded due to targeting localhost (normal for pihole), therefore waiting for a container url to come live is never going to happen !
