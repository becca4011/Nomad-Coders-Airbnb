const gulp = require("gulp")

const css = () => {
    const postCSS = require("gulp-postcss");
    const sass = require("gulp-sass");
    const minify = require("gulp-csso");
    sass.compiler = require("node-sass");

    return gulp
        // scss파일을 css파일로 변환
        .src("assets/scss/styles.scss")
        .pipe(sass().on("error", sass.logError))
        .pipe(postCSS([
            require("tailwindcss"),
            require("autoprefixer")
        ])) // assets/scss/styles.scss에서 tailwind를 css로 바꿔줌
        .pipe(minify()) // 코드를 짧게 만듦(파일 크기 작아짐)
        .pipe(gulp.dest("static/css")); // 결과를 static/css에 보냄
};

exports.default = css;