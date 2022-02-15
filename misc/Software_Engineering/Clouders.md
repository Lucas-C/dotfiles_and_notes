## aws CLI

    # Alt: achiku/jungle, donnemartin/saws
    aws configure # eu-west-1
    aws iam list-user-policies --user-name $USER # Also: aws iam list-roles
    aws s3 cp $file s3://$USER-pail/ # Other cmds: mb rb ls rm mv
    # AWS Lambda - mostly from http://alestic.com/mt/mt-search.cgi?blog_id=1&tag=AWS%20Lambda
    aws lambda list-functions
    aws lambda invoke-async --function-name $function --region us-east-1 --invoke-args inputfile.json --debug
    aws logs describe-log-groups --region us-east-1
    log_group_name=/aws/lambda/$function
    log_stream_names=$(aws logs describe-log-streams --region us-east-1 --log-group-name "$log_group_name" --output text --query 'logStreams[*].logStreamName')
    for stream in $log_stream_names; do
        aws logs get-log-events --region us-east-1 --log-group-name "$log_group_name" --log-stream-name "$stream" --output text --query 'events[*].message'
    done | less

## Heroku

    heroku login
    heroku create
    heroku logs -t # --ps worker.1
    Procfile # web: gunicorn gettingstarted.wsgi --log-file -
    heroku ps # list running dynos
    heroku releases # deployments log
    foreman start web # local run, once deps are installed
    heroku addons:open papertrail # CLI: heroku plugins:install https://github.com/papertrail/papertrail-heroku-plugin
    heroku run python manage.py shell
    heroku run bash
    heroku config # can be defined in .env
    heroku pg # PostgreSQL terminal summary dashboard
    heroku pg:psql
