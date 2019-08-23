# TwitterTweetAnalysis

## Basic Installation setup of the project on a mac
# Installing Python3 on a Mac
1. Start the terminal and type the following commands
2. `xcode-select --install`
3. `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
4. `brew install python3`


# Installing Apache Kafka on a Mac
1. Again, start the terminal and type the following commands
2. `brew cask install java`
3. `  brew cask install homebrew/cask-versions/adoptopenjdk8`
4. `brew install kafka`
5. `zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties`
6. `kafka-server-start /usr/local/etc/kafka/server.properties`
7. `kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <name of the topic>`
