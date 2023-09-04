const std = @import("std");

const converter = @import("converter");

const zglfw = @import("zglfw");
const zgpu = @import("zgpu");
const zgui = @import("zgui");

const ConverterErrors = error{
    WeirdGameDir,
};

pub fn main() !void {
    zglfw.init() catch {
        std.log.err("Failed to initialize GLFW library.", .{});
        return;
    };
    defer zglfw.terminate();

    const window = zglfw.Window.create(1600, 1000, "Legacy Mod Converter 1.0 for Pre-Release 5.2", null) catch {
        std.log.err("Failed to create window.", .{});
        return;
    };
    defer window.destroy();
    window.setSizeLimits(400, 400, -1, -1);

    var gpa_state = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa_state.deinit();
    const gpa = gpa_state.allocator();

    const gctx = try zgpu.GraphicsContext.create(gpa, window, .{});
    defer gctx.destroy(gpa);

    zgui.init(gpa);
    defer zgui.deinit();

    // _ = zgui.io.addFontFromFile("content/Roboto-Medium.ttf", 26.0);
    // _ = zgui.io.addFontFromFile("content/FiraCode-Medium.ttf", 26.0);
    _ = zgui.io.addFontFromFile("content/ProggyClean.ttf", 26.0);

    zgui.backend.init(
        window,
        gctx.device,
        @intFromEnum(zgpu.GraphicsContext.swapchain_format),
    );
    defer zgui.backend.deinit();

    while (!window.shouldClose()) {
        zglfw.pollEvents();

        zgui.backend.newFrame(
            gctx.swapchain_descriptor.width,
            gctx.swapchain_descriptor.height,
        );

        // Set the starting window position and size to custom values
        zgui.setNextWindowPos(.{ .x = 20.0, .y = 20.0, .cond = .first_use_ever });
        zgui.setNextWindowSize(.{ .w = -1.0, .h = -1.0, .cond = .first_use_ever });

        if (zgui.begin("Button list", .{})) {
            if (zgui.button("Convert", .{ .w = 200.0 })) {
                std.debug.print("Converting...\n", .{});

                var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
                defer arena.deinit();
                var allocator = arena.allocator();

                const cwd = std.fs.cwd();

                var input_mod_path_buffer: [std.fs.MAX_PATH_BYTES]u8 = undefined;
                // const input_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Mod-Converter-Engine/tests/mod/in", &input_mod_path_buffer);
                const input_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Community-Project-Data/LegacyModConverter-v1.0-pre5.2/Input", &input_mod_path_buffer);

                var output_mod_path_buffer: [std.fs.MAX_PATH_BYTES]u8 = undefined;
                // const output_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Mod-Converter-Engine/tests/mod/out", &output_mod_path_buffer);
                const output_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Community-Project-Data/Mods", &output_mod_path_buffer);

                var diagnostics: converter.Diagnostics = .{};
                converter.convert(
                    input_mod_path,
                    output_mod_path,
                    allocator,
                    &diagnostics,
                ) catch |err| switch (err) {
                    error.UnexpectedToken => {
                        const token = diagnostics.token orelse "null";
                        const file_path = diagnostics.file_path orelse "null";
                        const line = diagnostics.line orelse -1;
                        const column = diagnostics.column orelse -1;

                        std.debug.print("Error: Unexpected '{s}' at {s}:{}:{}\n", .{
                            token,
                            file_path,
                            line,
                            column,
                        });
                    },
                    error.TooManyTabs => {
                        const file_path = diagnostics.file_path orelse "null";
                        const line = diagnostics.line orelse -1;
                        const column = diagnostics.column orelse -1;

                        std.debug.print("Error: Too many tabs at {s}:{}:{}\n", .{
                            file_path,
                            line,
                            column,
                        });
                    },
                    else => |e| return e,
                };

                std.debug.print("Done converting!\n", .{});
            }
            if (zgui.button("Launch", .{ .w = 200.0 })) {
                const path = "I:/Programming/Cortex-Command-Community-Project-Data/Cortex Command.debug.release.exe";
                try std.os.chdir(std.fs.path.dirname(path) orelse return ConverterErrors.WeirdGameDir);
                var argv = [_][]const u8{path};
                const result = try std.ChildProcess.exec(.{ .argv = &argv, .allocator = gpa });
                _ = result;
            }
            if (zgui.button("Zip", .{ .w = 200.0 })) {
                var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
                defer arena.deinit();
                var allocator = arena.allocator();

                // TODO: Why am I using cwd.realpath()?

                const cwd = std.fs.cwd();

                var input_mod_path_buffer: [std.fs.MAX_PATH_BYTES]u8 = undefined;
                const input_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Community-Project-Data/LegacyModConverter-v1.0-pre5.2/Input", &input_mod_path_buffer);

                var output_mod_path_buffer: [std.fs.MAX_PATH_BYTES]u8 = undefined;
                const output_mod_path = try cwd.realpath("I:/Programming/Cortex-Command-Community-Project-Data/Mods", &output_mod_path_buffer);

                try converter.zip_mods(input_mod_path, output_mod_path, allocator);
            }
        }
        zgui.end();

        const swapchain_texv = gctx.swapchain.getCurrentTextureView();
        defer swapchain_texv.release();

        const commands = commands: {
            const encoder = gctx.device.createCommandEncoder(null);
            defer encoder.release();

            // GUI pass
            {
                const pass = zgpu.beginRenderPassSimple(encoder, .load, swapchain_texv, null, null, null);
                defer zgpu.endReleasePass(pass);
                zgui.backend.draw(pass);
            }

            break :commands encoder.finish(null);
        };
        defer commands.release();

        gctx.submit(&.{commands});
        _ = gctx.present();
    }
}
