package com.frame.entity;


import lombok.ToString;

@ToString
public class JsonResult {
    String data,message,code;
    public static JsonResult builder(){
        return new JsonResult();
    }
    public  JsonResult data(String data){
        this.data = data;
        return this;
    }
    public JsonResult message(String m){
        this.message = m;
        return this;
    }
    public JsonResult code(String c){
        this.code = c;
        return this;
    }
    public JsonResult build(){
        return this;
    }
}
