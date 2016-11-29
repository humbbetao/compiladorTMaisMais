; ModuleID = "Programa"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"printf_f"(float %".1") 

declare float @"scanf_f"(float %".1") 

@"global.a" = external global i32
@"global.b" = external global i32
@"global.c" = external global float
@"global.d" = external global float
define i32 @"novo"() 
{
entry:
  ret i32 2
}

define float @"main"() 
{
entry:
  %"principal.a" = alloca float
  %"principal.b" = alloca float
  %"principal.c" = alloca float
  %".2" = load float, float* %"principal.a"
  %".3" = load float, float* %"principal.b"
  %"addtmp" = fadd float %".2", %".3"
  %".4" = load float, float* %"principal.a"
  %".5" = call float (float) @"printf_f"(float %".4")
  %".6" = load float, float* %"principal.a"
  ret float %".6"
}
