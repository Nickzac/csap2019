# YANG MODEL PARSER
REQUIREMENTS
python libraries:pyang

If you are using this tool then you probably want to install the following python libraries(not required for the tool)

ydk
ydk-models-cisco-ios-xe

To install the libraries above follow those steps(TESTED ON MAC OS High Sierra):

{code}
git clone https://github.com/CiscoDevNet/ydk-gen.git -b 0.7.2
cd ydk-gen
./generate --libydk
[sudo] make -C gen-api/python/ydk install

# install ydk-py
[sudo] pip install ydk
{code}

Usage
python xml_parser.py <yang_model_file.yang> <variable to search>

TODO:
Search for files not only in the root directory

