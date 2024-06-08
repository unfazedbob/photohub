package com.frame.controller;

import com.alibaba.fastjson.JSON;
import com.frame.dao.PhotohubMapper;
import com.frame.entity.JsonResult;
import com.frame.entity.photo;
import com.frame.utils.dirUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Controller
public class test {


    @Autowired
    PhotohubMapper photoDao;



    @RequestMapping("/login")
    public String t2(){
        return "/login";
    }

    @RequestMapping(value = "/upload")
    public String t3(){
        return "/picUpload";
    }

    //图片上传处理（将路径保存到数据库）
    @RequestMapping(value = "/upload2",method = RequestMethod.POST)
    public void t4(@RequestParam("file") String pic) throws IOException {
        System.out.println(pic);//图片的二进制格式

        String currentDir = System.getProperty("user.dir");
        String fileName = "test.jpg";
        String filePath = currentDir + "/" + fileName;
        FileOutputStream fileOutputStream = new FileOutputStream(filePath);
        fileOutputStream.write(pic.getBytes());
    }

    /**
     * 时间格式化
     */
    private SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy/MM/dd/");

    /**
     * 图片保存路径，自动从yml文件中获取数据
     *   示例： E:/images/
     */

    @Value("${file-save-path}")
    private String fileSavePath;


    @PostMapping("/upload")
    @ResponseBody
    public String uploadFile(@RequestParam("file") MultipartFile file, HttpServletRequest request) {
        //后半段目录：  2020/03/15
        String directory = simpleDateFormat.format(new Date());
        /**
         * 文件保存目录  E:/images/2020/03/15/
         * 如果目录不存在，则创建
         */

        File dir = new File(fileSavePath + directory);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        String newFileName= file.getOriginalFilename();
        //创建这个新文件
        File newFile = new File(fileSavePath + directory + newFileName);
        //复制操作
        try {
            file.transferTo(newFile);
            //协议 :// ip地址 ：端口号 / 文件目录(/images/2020/03/15/xxx.jpg)
            String url = request.getScheme() + "://" + request.getServerName() + ":" + request.getServerPort() + "/images/" + directory + newFileName;
            System.out.println("图片上传，访问URL：" + url);
            //组装photo类
            photo ph = photo.builder().location(dirUtil.transDir(fileSavePath + directory + newFileName)).type("默认分类").owner_id(10086).build();
            //存入数据库
            photoDao.insertPhoto(ph);
            return JSON.toJSONString(JsonResult.builder().data(JSON.toJSONString(ph)).message("上传成功！").code("200").build());

        } catch (IOException e) {

            return JSON.toJSONString(JsonResult.builder().data(null).message("上传失败").code("500").build().toString());
        }
    }



    //查看所有图片
    @PostMapping("/allPhoto")
    @ResponseBody
    public String allPhoto() {
        List<photo> photos = photoDao.selectAllPhotoByOwnerID(10086);
        return JSON.toJSONString(photos);
    }

}

