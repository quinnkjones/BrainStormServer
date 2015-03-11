var app = angular.module('Mydea',[]);

app.controller('RestController', function($scope, $http) {
	$scope.urls = null;
	$http.get('/api').success(function(d){
		$scope.urls = d;
		$scope.ideas = null;
        
		$http.get($scope.urls.ideas).success(function(d){
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


app.controller('IdeaController',function($scope, $http, userFactory, transcriptionFactory){
	$scope.load_idea = function(url) {
		$http.get(url).success(function(d){
            console.log(d);
			$scope.idea = d;
            userFactory($scope.idea.user, $scope);
            transcriptionFactory($scope.idea.transcription, $scope);
		});
	};
});

app.factory('userFactory', function($http){
    function User(url, $scope){
        $http.get(url).success(function(data){
            $scope.idea.user = data;
        })
    }
    return User;
});

app.factory('transcriptionFactory', function($http){
    function Transcription(url, $scope){
        $http.get(url).success(function(data){
            $scope.idea.transcription = data.value;
        })
    }
    return Transcription
});

app.run(function($http) {
    $http.defaults.headers.common.Authorization = '6969';
    $http.defaults.cache = true;
});

