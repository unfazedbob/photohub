package com.frame.entity;


import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@Builder
public class photo {
  private   int id;
  private   int owner_id;
  private   String location;
  private   String comment;
  private   String type;

}
