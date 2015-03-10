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
    $scope.add_idea = function(idea){
        $http.post($scope.urls.ideas, {title: "", desc: idea});
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


app.controller('IdeaController',function($scope,$http){
	$scope.idea = null;
	$scope.load_media = function(url){
		$http.get(url).success(function(d){
			$scope.idea = d;
		});
	};
});

app.controller('CommentController', function($scope, $http){
    $scope.comment = null;
    $scope.init_comment = function(url){
        $http.get(url).success(function(data){
            $scope.comment = data;
        });
    };
});

app.controller('UserController', function($scope, $http){
    $scope.user = null;
    $scope.init_user = function(url){
        console.log(url);
        $http.get(url).success(function(data){
            $scope.user = data;
        });
    };
});

app.run(function($http) {
  $http.defaults.headers.common.Authorization = '6969';
});

