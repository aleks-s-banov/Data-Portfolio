*** Settings ***
Library     OperatingSystem
Library     RPA.Browser.Selenium



*** Keywords ***
Store the latest ${number_of_tweets} tweets by user name "${user_name}"
    Open Twitter homepage   ${user_name}
    Store tweets            ${user_name}    ${number_of_tweets}
    [Teardown]              Close Browser

Open Twitter homepage
    [Arguments]             ${user_name}   
    Open Browser     ${TWITTER_URL}/${user_name}     Chrome  

Store tweets
    [Arguments]                     ${user_name}            ${number_of_tweets}       
    ${tweets_locator}=              Get tweets locator      ${user_name}
    Wait Until Element Is Visible    ${tweets_locator}    timeout=10000
    @{tweets}=                      Get WebElements         ${tweets_locator}
    ${tweet_directory}=             Get tweet directory     ${user_name}
    Create Directory                ${tweet_directory}
    ${index}=                       Set Variable            1

    FOR     ${tweet}  IN  @{tweets}
        Exit For Loop If            ${index} > ${number_of_tweets}
        ${text_file}=               Set Variable    ${tweet_directory}/tweet-${index}.txt
        ${text}=                    Set Variable    ${tweet.find_element("xpath",".//div[@lang='en']").text}
        Create File                 ${text_file}    ${text}
        ${index}=                   Evaluate        ${index} + 1
        Sleep  3
    END

Get tweets locator
    [Arguments]     ${user_name}
    [Return]        xpath://article[descendant::span[contains(text(), "\@${user_name}")]]

Get tweet directory
    [Arguments]     ${user_name}
    [Return]        ${CURDIR}/output/tweets/${user_name}
