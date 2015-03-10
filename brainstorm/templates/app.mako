<!DOCTYPE html>
<html ng-app="Mydea">
    <head>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="${req.url('static', pathspec='css/app.css')}">
        <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
        <script src="${req.url('static', pathspec='lib/Mydea.js')}"></script>
    </head>
    <body ng-controller="RestController">
        <div class="left-info">
            <div class="brand">
                Mydea
            </div>
            <div class="user-info">
                <div class="acorn">
                    <div class="color" style="background: #00A0B0;"></div>
                    <div class="text">Brain Case</div>
                </div>
                <div class="acorn">
                    <div class="color" style="background: #6A4A3C;"></div>
                    <div class="text">WVU SNRC</div>
                </div>
                <div class="acorn">
                    <div class="color" style="background: #CC333F;"></div>
                    <div class="text">Best Team</div>
                </div>
            </div>
        </div>
        <div class="mid">
            <div class="top-bar">
                %if not req.user:
                    <div class="actions">
                        <a href="#">Login</a>
                        <div class="sep"></div>
                        <a href="#">Sign Up</a>
                    </div>
                %else:
                    <div class="actions">
                        ${req.user.username}
                        <div class="sep"></div>
                        <a href="#">Logout</a>
                    </div>
                %endif
                <div class="have-an-idea">
                    <button class="btn btn-primary">Record Idea</button>
                </div>
            </div>
            <div class="ideas">
                <div class="idea" ng-repeat="idea_url in ideas" ng-controller="IdeaController" ng-init="load_idea(idea_url)">
                    <div class="likes">
                        <a class="like" ng-click="idea.likes = idea.likes + 1;"><i class="fa fa-caret-up fa-lg"></i></a>
                        <div class="like-count">{{idea.likes}}</div>
                        <a class="dislike" ng-click="idea.likes = idea.likes - 1"><i class="fa fa-caret-down fa-lg"></i></a>
                    </div>
                    <div class="avatar" ng-controller="UserController" ng-init="init_user(idea.user)">
                        <img ng-src="{{user.gravatar}}">
                    </div>
                    <div class="details">
                        <div class="poster">
                            Posted by <a href="#">Quinn</a> in <a href="#">BrainCase</a>
                        </div>
                        <div class="transcription">
                            <i>No transcription available</i>
                        </div>
                        <div class="actions">
                            <a><i class="fa fa-play-circle"></i></a>
                            <a><i class="fa fa-comment"></i></a>
                            <i class="comment-count">0 comments</i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="right-bar">
            <div class="padding">
            </div>
        </div>
    </body>
</html>