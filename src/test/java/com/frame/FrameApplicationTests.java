package com.frame;

import com.frame.dao.PhotohubMapper;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@SpringBootTest
@RunWith(SpringRunner.class)
public class FrameApplicationTests {

    @Autowired
    PhotohubMapper photohubMapper;

    @Test
    public void contextLoads() {
        System.out.println(photohubMapper.selectAllPhotoByOwnerID(10086));
    }

}
