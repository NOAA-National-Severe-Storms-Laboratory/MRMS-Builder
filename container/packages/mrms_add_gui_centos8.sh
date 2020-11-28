# Toomey Sept 2020

# -------------------------------------------------------------
# WDSS2 WG extras

# Use the xpra org repository.  We might even try using
# xpra in containers at some point for running wg
# it avoids some of the x display security stuff

# Web probably better but I'll hard cat it for now
# We're pulling over web from that repo anyway so it needs to be there
#curl https://xpra.org/repos/CentOS/xpra.repo -o /etc/yum.repos.d/xpra.repo
cat >/etc/yum.repos.d/xpra.repo <<'EOL'
[xpra]
name=Xpra $releasever - $basearch
enabled=1
metadata_expire=1d
gpgcheck=1
gpgkey=https://xpra.org/gpg.asc
baseurl=https://xpra.org/dists/CentOS/$releasever/$basearch/
EOL

dnf install gtkglext-devel -y


