import { Injectable, UnauthorizedException } from '@nestjs/common';
import { LoginDto, RegisterDTO } from './dto/auth.dto';
import { UsersService } from '../users/users.service';
import { JwtService } from '@nestjs/jwt';  // ← this, not JwtStrategy

@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,  // ← this
  ) {}
  
async register(dto: RegisterDTO){

  const user = await this.usersService.create(dto.firstName, dto.lastName,dto.email,dto.password)
  return this.buildResponse(user.id, user.firstName, user.lastName, user.email)

}
  async login(dto: LoginDto) {
    const user = await this.usersService.validateCredentials(dto.email, dto.password);
    if (!user) throw new UnauthorizedException('Invalid credentials');
    return this.buildResponse(user.id, user.firstName, user.lastName, user.email);
  }
 

private buildResponse(id: number, firstName: string, lastName, email: string){
const token = this.jwtService.sign({ sub: id, email, firstName, lastName });
    return { accessToken: token, user: { id, firstName,lastName, email } };
  }


}

