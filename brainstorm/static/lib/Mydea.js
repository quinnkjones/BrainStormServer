var app = angular.module('Mydea',['ngAudio']);

app.controller('RestController', function($scope, $http) {
	$scope.urls = null;
	$http.get('/api').success(function(d){
		$scope.urls = d;
		$scope.ideas = null;
        
		$http.get($scope.urls.ideas, {cache: false}).success(function(d){
			$scope.ideas = d;
		}); 
	});
    $scope.add_idea = function(){
        $http.post($scope.urls.ideas);
    };
});

app.controller('MediaController', function($scope,$http){
    $scope.media = null;
    $scope.load_media = function(url){
        $http.get(url).success(function(d){
            $scope.media = d;
        });
    };
});


app.controller('IdeaController',function($scope, $http, userInitService, trsInitService, mediaListService){
	$scope.load_idea = function(url) {
		$http.get(url).success(function(d){
            console.log(d);
			$scope.idea = d;
            userInitService.init_user($scope.idea.user, $scope);
            trsInitService.init_transcription($scope.idea.transcription, $scope);
            mediaListService.init_media($scope.idea.media.slice(), $scope);
		});
	};
});

app.service('userInitService', function($http){
    this.init_user = function(url, $scope){
        $http.get(url).success(function(data){
            $scope.idea.user = data;
        })
    };
});

app.service('trsInitService', function($http){
    this.init_transcription = function(url, $scope){
        $http.get(url).success(function(data){
            $scope.idea.transcription = data.value;
        })
    };
});

app.service('mediaListService', function($http, ngAudio) {
    function MediaObj(url, $scope){
        var _this = this;
        this.load = function(){
            console.log("Getting " + url);
            $http.get(url).success(function(data){
                for(var i in data){
                    if(data.hasOwnProperty(i)){
                        _this[i] = data[i];
                    }
                }
                if(data.type === 2){
                    _this.sound = ngAudio.load(data.value);
                }
            });
        }
    }
    this.init_media = function(media, $scope){
        $scope.idea.media = [];
        for(var c = 0; c < media.length; c++){
            $scope.idea.media[c] = new MediaObj(media[c], $scope);
        }
    };
});

app.run(function($http) {
    $http.defaults.headers.common.Authorization = '6969';
    $http.defaults.cache = true;
});

