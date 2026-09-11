module empty_tb;
  integer c;
  initial begin
    $display("READY");
    $fflush();
    c = $fgetc(32'h8000_0000);
  end
endmodule
