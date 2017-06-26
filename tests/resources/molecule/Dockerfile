FROM phusion/baseimage:0.9.22
LABEL maintainer "Alexandre Chaussier <a.chaussier@infopen.pro>"

# Use base image init system
CMD ["/sbin/my_init"]

# Enable SSHd daemon
RUN rm -f /etc/service/sshd/down

# Regenerate SSH host keys
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use base image insecure key to login
RUN /usr/sbin/enable_insecure_key

# Install Python 2.7, sudo , manage a /usr/bin/python link and clean APT cache
RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            python2.7=2.7.12* \
            sudo=1.8.16* \
        && ln -s /usr/bin/python2.7 /usr/bin/python \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Expose SSHd port
EXPOSE 22
