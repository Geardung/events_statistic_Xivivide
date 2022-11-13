import os

from main import start_parsing

os.system('dotnet /home/exporter/DiscordChatExporter.Cli.dll export -c 904020811625672714 -t NjQwNzk3NTA4NjQ5NjE1Mzgw.G-gUqI.YUVqKUidrhL5P3kz_hqnckRduhrUmxfZW8teoU -o /home/HTMLparsing/in/parsed.json -f JSON --after "2022-09-01 00:00"')

print("exported")

start_parsing(True)