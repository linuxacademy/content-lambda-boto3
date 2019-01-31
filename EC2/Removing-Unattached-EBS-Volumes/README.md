# Removing Unattached EBS Volumes

When an instance is terminated, EC2 uses the value of the `DeleteOnTermination` attribute for each attached EBS volume to determine whether to preserve or delete the volume when the instance is terminated.

By default, the `DeleteOnTermination` attribute for the root volume of an instance is set to `true`, but it is set to `false` for all other volume types.

To preserve the root volume when an instance is terminated, change the `DeleteOnTermination` attribute for the root volume to `false`.

## Changing the root volume of a running instance to persist

1. Edit `mapping.json`, setting the value for `DeviceName` to your block device name.

2. Using the AWS CLI, modify the `DeleteOnTermination` attribute:

    ```sh
    aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 --block-device-mappings file://mapping.json
    ```

More info: [Preserving Amazon EBS Volumes on Instance Termination](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#preserving-volumes-on-termination)