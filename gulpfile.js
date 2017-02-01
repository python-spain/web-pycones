'use strict';
var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var rename = require("gulp-rename");
var imagemin = require('gulp-imagemin');
var cssnano = require('gulp-cssnano');
var pixrem = require('gulp-pixrem');
var babel = require('gulp-babel');
var browserify = require('gulp-browserify');

var config = require('./package.json');


// Helper for handle static paths
// -----------------------------------------------------------------------------
var pathsConfig = function (appName) {
  var app = appName || config.name;
  return {
    app: app,
    templates: app + '/templates',
    base: app + '/static',
    sass: app + '/static/sass',
    css: app + '/static/css',
    fonts: app + '/static/fonts',
    images: app + '/static/images',
    js: app + '/static/js',
    manageScript: app + 'manage.py'
  }
};


// CSS Task
// -----------------------------------------------------------------------------
var cssTask = function (options) {

  // Default include node_modules to SASS include paths
  var sassOptions = {
    includePaths: ['./node_modules/'],
    errLogToConsole: true
  };

  // Common 'run' code for each options
  var run = function (options) {
    options = sassOptions || options;
    gulp.src(pathsConfig().sass + '/pycones.scss')
      .pipe(sass(options).on('error', sass.logError))
      .pipe(autoprefixer({browsers: ['last 2 version']}))
      .pipe(pixrem())
      .pipe(gulp.dest(pathsConfig().css))
      .pipe(rename({ suffix: '.min' }))
      .pipe(cssnano())
      .pipe(gulp.dest(pathsConfig().css));
  };

  // Run for development with watch
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
    // Run for production with compressed
  } else {
    run({outputStyle: 'compressed'});
  }

};


// Images Task
// -----------------------------------------------------------------------------
var imagesTask = function (options) {
  var run = function () {
    gulp.src(pathsConfig().images + '/**/*')
      .pipe(imagemin())
      .pipe(gulp.dest(pathsConfig().images));
  };
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
  } else {
    run();
  }
};


// App Task
// -----------------------------------------------------------------------------
var appTask = function (options) {
  var run = function () {
    gulp.src(pathsConfig().js + '/src/*.js')
      .pipe(babel({presets: ['es2015']}))
      .pipe(browserify({insertGlobals: true}))
      .pipe(rename('bundle.js'))
      .pipe(gulp.dest(pathsConfig().js + '/bin'));
  };
  if (options.development) {
    run();
    gulp.watch(options.watch, run);
  } else {
    run();
  }
};

// Default Task
// -----------------------------------------------------------------------------
// Starts our development workflow
gulp.task('default', function () {
  cssTask({
    watch: pathsConfig().sass + "/**/*.scss",
    development: true
  });
  imagesTask({
    development: false
    // watch: pathsConfig().images + "/**/*"
  });
  appTask({
    development: true,
    watch: pathsConfig().js + "/src/**/*"
  });
});


// Build Task
// -----------------------------------------------------------------------------
gulp.task('build', function () {
  cssTask({
    development: false
  });
  imagesTask({
    development: false
  });
  appTask({
    development: false
  });
});

