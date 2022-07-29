class MetasploitModule < Msf::Encoder
    Rank = NormalRanking

    def initialize
        super(
          'Name'             => 'Bash Base64 Encoder',
          'Description'      => %q{
            Base64 encodes bash scripts.
          },
          'Author'           => 'An Ethical Hacker',
        )
    end
  
    def encode_block(state, buf)
        unicode = Rex::Text.to_unicode(buf)
        base64 = Rex::Text.encode_base64(unicode)
        cmd = "base64 -d <<< #{base64} | sh"
        return cmd
    end
    
