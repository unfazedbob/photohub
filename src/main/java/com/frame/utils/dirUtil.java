package com.frame.utils;

public class dirUtil {
    //将形如 "/a/b/c" 的目录转换为 "a//b//c" 便于前端展示
    public static String transDir(String dir){
        return dir.replace("/","//");
    }
}
