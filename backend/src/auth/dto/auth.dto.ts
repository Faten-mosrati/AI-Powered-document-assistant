import { IsEmail, IsNotEmpty, IsString, MaxLength, MinLength } from "class-validator"

export class RegisterDTO {

@IsString()
@IsNotEmpty()
@MinLength(3)
@MaxLength(30)
firstName : string; 

@IsString()
@IsNotEmpty()
@MinLength(3)
@MaxLength(30)
lastName: string;

@IsEmail()
email: string; 

@IsString() @MinLength(8) @MaxLength(72)
password
}


export class LoginDto {
  @IsEmail()
  email: string;
 
  @IsString() @IsNotEmpty()
  password: string;
}
 