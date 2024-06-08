package com.frame.dao;

import com.frame.entity.photo;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface PhotohubMapper {
    //信息存入数据库
    void insertPhoto(photo ph);

    //查出指定owner_id的所有照片
    List<photo> selectAllPhotoByOwnerID(int owner_id);
}
