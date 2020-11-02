mkdir -p ~/.equador-v1/

echo "\
[general]\n\
email = \"neverrox@gmail.com\"\n\
" > ~/.equador-v1/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.equador-v1/config.toml