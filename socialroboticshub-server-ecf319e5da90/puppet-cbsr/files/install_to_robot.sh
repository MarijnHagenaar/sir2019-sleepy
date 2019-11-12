#!/usr/bin/env bash

read -rp "Enter the robot's IP address: " robot_ip
if ! ping -c 1 "$robot_ip" &> /dev/null; then
  echo "$robot_ip is unreachable."
  exit 1
else
  echo "Connection successful!"
fi

echo "Updating config files..."
read -rp "Enter your machine's main IP address: " server_ip
cp -f /opt/processing/webserver/config.json.template /opt/processing/webserver/config.json
sed -i "s/127.0.0.1/$server_ip/" /opt/processing/webserver/config.json
cp -f /var/puppet-cbsr/files/start.sh.template /var/puppet-cbsr/files/start.sh
sed -i "s/unknown/$server_ip/" /var/puppet-cbsr/files/start.sh

echo "Please enter the password whenever prompted!"

# Create the folder for all files on the robot
target_dir="/home/nao/cbsr"
echo "Creating $target_dir if it does not exist."
# $target_dir should expand client-side
# shellcheck disable=SC2029
ssh nao@$robot_ip "mkdir -p $target_dir"

# Collect all of the files to copy
scp_files=()
scp_files+=("$(find /opt/input/robot_microphone -name "robot_sound_processing.py")")
scp_files+=("$(find /opt/input/robot_camera -name "visual_producer.py")")
scp_files+=("$(find /opt/input/robot_touch -name "event_producer.py")")
scp_files+=("$(find /opt/output/robot_actions -name "action_consumer.py")")
scp_files+=("$(find /opt/output/robot_tablet -name "tablet.py")")
scp_files+=("$(find /opt/output/robot_tablet -name "tablet_consumer.py")")
scp_files+=("$(find /var/puppet-cbsr/files -name "start.sh")")
scp_files+=("$(find /var/puppet-cbsr/files -name "stop.sh")")
# SCP them away
echo "Copying files to the robot..."
scp -p "${scp_files[@]}" nao@$robot_ip:$target_dir/

echo "Done!"
echo ""

read -p "Are you going to use the tablet or play audio? (y/n) " answer1
case ${answer1:0:1} in
    y|Y )
        sudo service webserver restart
    ;;
    * )
        sudo service webserver stop
    ;;
esac

read -p "Are you going to use face recognition? (y/n) " answer2
case ${answer2:0:1} in
    y|Y )
        sudo service video_facerecognition restart
    ;;
    * )
        sudo service video_facerecognition stop
		read -p "Are you going to use people detection? (y/n) " answer2b
		case ${answer2b:0:1} in
			y|Y )
				sudo service video_peopledetection restart
			;;
			* )
				sudo service video_peopledetection stop
			;;
		esac
    ;;
esac

read -p "Are you going to use DialogFlow? (y/n) " answer3
case ${answer3:0:1} in
    y|Y )
        sudo service audio_dialogflow restart
    ;;
    * )
        sudo service audio_dialogflow stop
		read -p "Are you going to use Google STT? (y/n) " answer3b
		case ${answer3b:0:1} in
			y|Y )
				sudo service audio_google restart
			;;
			* )
				sudo service audio_google stop
			;;
		esac
    ;;
esac

read -p "Are you going to use web searches? (y/n) " answer4
case ${answer4:0:1} in
    y|Y )
        sudo service websearch restart
    ;;
    * )
        sudo service websearch stop
    ;;
esac