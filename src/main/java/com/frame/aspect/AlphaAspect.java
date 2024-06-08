package com.frame.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

@Configuration
@Aspect
public class AlphaAspect {

    //定义切点
    @Pointcut("within(com.frame.controller..*)")
    public void pointcut() {

    }

    //各种位置的切点处理
    @Before("pointcut()")
    public void before() {
        //System.out.println("before");
    }

    @After("pointcut()")
    public void after() {
        //System.out.println("after");
    }

    @AfterReturning("pointcut()")
    public void afterRetuning() {
        //System.out.println("afterRetuning");
    }

    @AfterThrowing("pointcut()")
    public void afterThrowing() {
        //System.out.println("afterThrowing");
    }

    @Around("pointcut()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        //System.out.println("around before");
        Object obj = joinPoint.proceed();
        //System.out.println("around after");
        return obj;
    }

}
