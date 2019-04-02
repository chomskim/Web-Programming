//
// Vector2D Class Definition -- Vector2D in Java3D
// Programmed By cskim in HUFS 2012.4.24
//

function Vector2d(x, y){
	this.x = x;
	this.y = y;
	
	this.add = function(v1) {
		this.x += v1.x;
		this.y += v1.y;
		return this;
	}
	this.sub = function(v1) {
		this.x -= v1.x;
		this.y -= v1.y;
		return this;
	}
	this.equals = function(v1) {
		return this.x == v1.x && this.y == v1.y;
	}
	this.scale = function(s) {
		this.x *= s;
		this.y *= s;
		return this;
	}
	this.dot = function(v1){
		return this.x*v1.x + this.y*v1.y;
	}
	this.length = function() {
		return Math.sqrt(this.x*this.x + this.y*this.y);
	}
	this.normalize = function() {
		var leng = this.length();
		if (leng!=0){
			this.x /= leng;
			this.y /= leng;
		}
		return this;
	}
	this.angle = function(v1) {
		return Math.acos(this.dot(v1)/(this.length()*v1.length()));
	}
}