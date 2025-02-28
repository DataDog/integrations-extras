# Gambit MIMIC Simulator

## Overview

MIMIC Simulator is a dynamic, real-time, high-performance SNMP, Netflow, sFlow Simulator. All Netflow and sFlow exports are recorded by the simulator and replayed with flexible customization toward Datadog agent(s) and presented with all existing available metrics of Datadog, whether built-in or Datadog marketplace integrated.

Large enterprises use MIMIC in the lab to customize Datadog dashboards, to test modifications with expected
and unexpected scenarios, and to train operators prior to deployment in mission-critical production environments.

## Setup

## MIMIC Installation Instructions

### [Overview]()

MIMIC is distributed as a compressed file for each platform, either on CD-ROM or downloadable from the Web. This file needs to be uncompressed and its contents extracted on your system.

Follow the below 3 steps to install.

After installation, please review the [MIMIC Frequently Asked Questions page][1].

**NOTE: you only need to download MIMIC when a new release is issued.**\
The evaluation and purchased versions are identical except for the license keys. If you have already downloaded MIMIC, determine the version you are running (eg. in MIMICview `Help->About Mimic...` or by looking at the contents of the `config/version` file), and download again only if the distribution listed below is newer.

#### Step 1: Get the MIMIC distribution

If you have a CD-ROM, copy the distribution file for your platform from the CD-ROM to a temporary directory. Go to Step 2.

To download from the Web from a URL that Gambit has provided, save the distribution files for your desired platform to a temporary directory (use right mouse-button click on the link for most web browsers).

**NOTE: make sure the entire file was downloaded and verify size.**

**NOTE: there are scam versions of any software floating around the Internet with all sorts of malware. Download only authoritative versions of MIMIC from a URL that Gambit has given you directly.**

#### Step 2: Uncompress and extract the distribution files

-   For Windows:\
    Run the self-extracting mimic-windows.exe from an Administrator account.

-   For Linux:\
    `gunzip -c mimic-linux.tar.gz | tar xf -`

    The extracted files are:

    README - further release-specific instructions\
    license.txt - the license agreement\
    install - the installation script\
    mimic.tar - the product

You are not done, please review the instructions in the next step.

#### Step 3: Further instructions

-   If you are **updating from an older release**

    -   make sure you **terminate MIMIC** (use `File->Terminate`) before running the install program.

    -   **Do not uninstall the older release** (this way you can always fallback in case of problems).

    -   Install this release in a **different directory from the older release**. MIMIC installs in these folders by default:

        -   Windows: `C:\Apps\Mimic.VERSION-NUMBER` eg. `C:\Apps\Mimic.1800`

        -   Linux: `/usr/local/mimic`

            On Linux you can rename old install folder as:

            ```
            mv /usr/local/mimic /usr/local/mimic.old
            ```

            Then install in the default folder `/usr/local/mimic`.

    -   You only need to **apply your license keys** and start the new MIMIC. New license keys are only necessary if the old ones don't work. All your MIMIC data files will be fetched out of your existing [private area][2] .

    -   When you start MIMICView from the new version, all your MIMIC data files will be fetched out of your existing [private area][2] which usually resides in a directory named `mimic` under the user's HOME directory, and is displayed in the title bar of MIMICView. We recommend to backup this private data often (see this [FAQ][4] ).

    -   Additionally, you may need to **upgrade any optional packages**, such as MIBs, Device Library and Network Library if you were using them in older release. They can be downloaded and installed using the [Wizard->Update][5] menu. The Update Wizard preselects packages from your older version to install them in your new version.

-   If you are **installing for the first time**, the MIMIC installation program will display the HostID to be used in your evaluation license key request.

-   If you are installing a Simulator other than SNMP, then you will have received **Get Started** instructions to download optional packages with sample simulations. Please refer to your [Get Started][6] instructions.

## Uninstallation

In Windows, use Start->MIMIC Simulator->Uninstall

## Support

support@gambitcomm.com


[1]: http://www.gambitcomm.com/faq
[2]: quick.htm#quick_private
[4]: faq.htm#backup_mimic
[5]: wizards.htm#updwiz
[6]: http://www.gambitcomm.com/getstarted/